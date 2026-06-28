from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView  # Yönlendirme (Redirect) modülü eklendi
import re

# Wagtail importları
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import views as wagtail_views

@require_POST
def custom_set_language(request):
    """
    Django'nun set_language view'ının yerini alır.
    Sorun: Django'nun yerleşik set_language'ı translate_url(next_url, lang_code) kullanır.
    Fakat /i18n/set_language/ prefix'siz bir URL olduğundan LocaleMiddleware aktif dili
    'tr' olarak zorlar. Bu durumda translate_url('/ru/', 'ru') -> resolve('/ru/') 'tr'
    aktif diliyle Wagtail serve view'ı olarak tanımlar.
    Çözüm: translate_url çağırmadan direkt `next` URL'sine yönlendir.
    """
    next_url = request.POST.get('next') or '/'
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = '/'
    response = HttpResponseRedirect(next_url)
    lang_code = request.POST.get('language')
    if lang_code and check_for_language(lang_code):
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=request.is_secure(),
            httponly=getattr(settings, 'LANGUAGE_COOKIE_HTTPONLY', False),
            samesite=getattr(settings, 'LANGUAGE_COOKIE_SAMESITE', 'Lax'),
        )
    return response

@never_cache
def root_language_handler(request):
    """
    Anasayfaya (/) gelen isteği yakalar ve dil ön ekine (örnek: /tr/, /en/) yönlendirir.
    """
    supported_codes = [l[0] for l in settings.LANGUAGES]
    default_lang = settings.LANGUAGE_CODE  # 'tr'

    # 1. Cookie - kullanıcının set_language POST ile kaydettiği dil tercihi
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, '').split('-')[0].lower()
    if cookie_lang:
        if cookie_lang in supported_codes:
            return redirect(f'/{cookie_lang}/')
        return redirect(f'/{default_lang}/')

    # 2. Accept-Language başlığı tarayıcı dil tercihi
    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for part in accept.split(','):
        m = re.match(r'([a-zA-Z]+)', part.strip())
        if not m:
            continue
        lang = m.group(1).lower()
        if lang in supported_codes:
            return redirect(f'/{lang}/')

    # 3. Eşleşen dil yok -> default dil ön eki
    return redirect(f'/{default_lang}/')

# 2. STANDART URL'LER
urlpatterns = [
    path('i18n/setlang/', custom_set_language, name='custom_set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

# 3. STATİK DOSYALAR (DEBUG Modu)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 4. KÖK YAKALAYICI
urlpatterns += [
    path('', root_language_handler, name='root_language_handler'),
]

# 5. DİĞER SAYFALAR İÇİN WAGTAIL VE I18N (/tr/, /en/, /ar/ vb.)
# prefix_default_language=True yaparak varsayılan dil olan Türkçe için de ön ek (/tr/) kullanılmasını zorunlu kılıyoruz.
# Böylece diller arası çakışmalar ve tarayıcı dilinden kaynaklı yönlendirme hataları tamamen çözülür.
urlpatterns += i18n_patterns(
    path('search/', include('crm.urls')), 
    path('', include('crm.urls')), 
    path('', include(wagtail_urls)),
    
    prefix_default_language=True,
)