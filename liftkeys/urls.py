from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.utils import translation

# Wagtail importları
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import views as wagtail_views # Wagtail görünümü

# 🔥 1. ÖZEL KARŞILAMA FONKSİYONU
def root_language_handler(request):
    """
    Anasayfaya (/) gelen isteği yakalar.
    - Tarayıcı dili Türkçe değilse (örn: İngilizce) -> /en/ adresine yönlendirir.
    - Tarayıcı dili Türkçe ise -> Olduğu yerde (yönlendirmeden) Wagtail sayfasını gösterir.
    """
    # 1. Tarayıcının istediği dili bul (Header veya Cookie'den)
    lang = translation.get_language_from_request(request)

    # 2. Eğer dil varsayılan (TR) değilse ve desteklenen bir dilse yönlendir
    if lang != settings.LANGUAGE_CODE and lang in [l[0] for l in settings.LANGUAGES]:
        return redirect(f'/{lang}/')

    # 3. Eğer dil Türkçe ise, Wagtail'ın sayfayı sunmasına izin ver
    # Wagtail'ın 'serve' fonksiyonunu manuel çağırıyoruz
    return wagtail_views.serve(request, request.path)


# 2. STANDART URL'LER
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

# 3. STATİK DOSYALAR (DEBUG Modu)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 4. KÖK DİZİN YAKALAYICI (En Önemli Kısım)
# i18n_patterns içine girmeden önce anasayfayı biz yakalıyoruz.
urlpatterns += [
    # Sadece boş '' (anasayfa) için özel fonksiyonumuzu çalıştır
    path('', root_language_handler, name='root_language_handler'),
]

# 5. DİĞER SAYFALAR İÇİN WAGTAIL VE I18N
urlpatterns += i18n_patterns(
    path('search/', include('crm.urls')), # Varsa search vb.
    path('', include('crm.urls')), 
    
    # Not: Buradaki Wagtail path'i artık anasayfayı ('') yakalamayacak 
    # çünkü yukarıda biz yakaladık. Alt sayfaları yakalayacak.
    path('', include(wagtail_urls)),
    
    prefix_default_language=False,
)