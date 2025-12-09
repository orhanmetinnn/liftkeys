from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.utils import translation

# Wagtail importları
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# CRM uygulamasından import
from crm.views import indexpage

# 🌍 Dil Yönlendirme Fonksiyonu
def language_or_index(request):
    user_language = translation.get_language_from_request(request)
    if user_language not in dict(settings.LANGUAGES):
        user_language = settings.LANGUAGE_CODE
    
    # Eğer zaten dil prefixi varsa döngüye sokma
    if request.path.startswith(f"/{user_language}/"):
        return redirect(request.path)

    # Varsayılan dil ise ana sayfayı aç
    if user_language == settings.LANGUAGE_CODE:
        return indexpage(request)

    # Değilse dile yönlendir
    return redirect(f'/{user_language}/')


# 1. Standart URL'ler (Dil eki almayanlar)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # Ana sayfa (Root) yakalayıcı
    path('', language_or_index),
]

# 2. Resim ve Statik Dosyalar (DEBUG Modunda)
# 🔥 EN ÖNEMLİ KISIM BURASI: Wagtail'dan önce tanımlanmalı!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 3. Çok Dilli URL'ler (En son Wagtail gelir)
urlpatterns += i18n_patterns(
    path('', include('crm.urls')),
    path('', include(wagtail_urls)), # Wagtail hepsini yakalar, en sonda olmalı
    prefix_default_language=False,
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)