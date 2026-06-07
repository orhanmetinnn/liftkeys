from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from django.views.decorators.http import require_POST
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

    Sorun: Django'nun yerleşik set_language'ı translate_url(next_url, lang_code) çağırır.
    Fakat /i18n/set_language/ prefix'siz bir URL olduğundan LocaleMiddleware aktif dili
    'tr' olarak zorlar. Bu durumda translate_url('/ru/', 'ru') → resolve('/ru/') 'tr'
    aktif diliyle Wagtail serve view'ı olarak tanımlar (args=('ru/',)) → reverse ile
    '/ru/ru/' çift prefix oluşur.

    Çözüm: translate_url çağırmadan direkt `next` URL'sine yönlendir.
    `change_lang` template tag'i doğru hedef URL'yi zaten üretmektedir.
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
            secure=getattr(settings, 'LANGUAGE_COOKIE_SECURE', False),
            httponly=getattr(settings, 'LANGUAGE_COOKIE_HTTPONLY', False),
            samesite=getattr(settings, 'LANGUAGE_COOKIE_SAMESITE', 'Lax'),
        )
    return response


def root_language_handler(request):
    """
    Anasayfaya (/) gelen isteği yakalar.

    NOT: translation.get_language() KULLANILMAZ çünkü Django'nun LocaleMiddleware'i
    prefix_default_language=False olduğunda prefix'siz tüm URL'leri zorla 'tr' yapar
    — Accept-Language ve cookie'ye bakmaz. Bu yüzden request'i kendimiz okuyoruz.

    Öncelik sırası:
    1. Cookie (set_language POST ile kullanıcının kaydettiği tercih)
    2. Accept-Language başlığı (tarayıcı dili)
    3. Desteklenmeyen dil → /en/ fallback

    - tr (varsayılan dil) → doğrudan Wagtail sayfasını serve et (prefix yok)
    - Desteklenen başka dil → /{lang}/ adresine yönlendir
    - Desteklenmeyen dil / eşleşme yok → /en/ adresine yönlendir
    """
    supported_codes = [l[0] for l in settings.LANGUAGES]
    default_lang = settings.LANGUAGE_CODE  # 'tr'

    # 1. Cookie — kullanıcının set_language POST ile kaydettiği dil tercihi
    cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, '').split('-')[0].lower()
    if cookie_lang:
        if cookie_lang == default_lang:
            return wagtail_views.serve(request, request.path)
        if cookie_lang in supported_codes:
            return redirect(f'/{cookie_lang}/')
        return redirect('/en/')  # desteklenmeyen cookie değeri → İngilizce

    # 2. Accept-Language başlığı — tarayıcı dil tercihi
    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for part in accept.split(','):
        m = re.match(r'([a-zA-Z]+)', part.strip())
        if not m:
            continue
        lang = m.group(1).lower()
        if lang == default_lang:
            return wagtail_views.serve(request, request.path)
        if lang in supported_codes:
            return redirect(f'/{lang}/')

    # 3. Eşleşen dil yok → /en/ fallback
    return redirect('/en/')


# 2. STANDART URL'LER (Yönlendirmeyi Buradan Kaldırdık!)
urlpatterns = [
    # Özel set_language: translate_url çağırmaz, change_lang'ın ürettiği URL'yi direkt kullanır
    # Django'nun yerleşik URL'si /i18n/setlang/ olduğundan bu path ÖNCE gelmelidir
    path('i18n/setlang/', custom_set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    # RedirectView silindi. Artık /tr/ otomatik olarak / adresine YÖNLENDİRİLMEYECEK.
]


# 3. STATİK DOSYALAR (DEBUG Modu)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# 4. KÖK DİZİN YAKALAYICI
urlpatterns += [
    path('', root_language_handler, name='root_language_handler'),
]


# 5. 🔥 /tr/ İÇİN MANUEL TANIMLAMA (Yeni Eklenen Bölüm)
# i18n_patterns /tr/ ekini unuttuğu için, /tr/ ile gelen istekleri 
# 404 hatasına düşmemesi adına manuel olarak Wagtail ve CRM'e bağlıyoruz.
urlpatterns += [
    path('tr/search/', include('crm.urls')),
    path('tr/', include('crm.urls')),
    path('tr/', include(wagtail_urls)),
]


# 6. DİĞER SAYFALAR İÇİN WAGTAIL VE I18N (/en/, /ar/ vb.)
urlpatterns += i18n_patterns(
    path('search/', include('crm.urls')), 
    path('', include('crm.urls')), 
    path('', include(wagtail_urls)),
    
    # Türkçe için otomatik ön eki iptal eder (Ana sayfanın düz / açılmasını sağlar)
    prefix_default_language=False,
)