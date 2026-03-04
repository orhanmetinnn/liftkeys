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
from wagtail import views as wagtail_views

# 🔥 1. ÖZEL KARŞILAMA FONKSİYONU (Senin Kodun)
def root_language_handler(request):
    """
    Anasayfaya (/) gelen isteği yakalar.
    - Tarayıcı dili Türkçe değilse (örn: İngilizce) -> /en/ adresine yönlendirir.
    - Tarayıcı dili Türkçe ise -> Olduğu yerde (yönlendirmeden) Wagtail sayfasını gösterir.
    """
    lang = translation.get_language_from_request(request)

    if lang != settings.LANGUAGE_CODE and lang in [l[0] for l in settings.LANGUAGES]:
        return redirect(f'/{lang}/')

    return wagtail_views.serve(request, request.path)


# 2. STANDART URL'LER (Yönlendirmeyi Buradan Kaldırdık!)
urlpatterns = [
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