from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings
from django.utils import translation
from wagtail.models import Locale
from .models import ProductPage

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return [
            'indexpage', 'contact', 'about','gizlilikguvenlik','category_list',
            "atlas_overload","horus_photocell","switch_systems",
            "zemin_view","fan_view","paten_view","solid_view",
            "kupeste_view","takozlar_view","gallery_view",
            "kagittanisleri_view","keys_view","kabincam_view", "patenkabin_view"
        ]

    def location(self, item):
        return reverse(item)

    # Django'nun kendi sitemap motoruna "Bu sayfanın alternatif dilleri var" diyoruz
    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        domain = site.domain if site else '127.0.0.1:8000'
        proto = protocol or 'http'

        for url_info in urls:
            item = url_info['item']
            alternates_list = []
            
            for lang_code, _ in settings.LANGUAGES:
                with translation.override(lang_code):
                    path = reverse(item)
                    alt_loc = f"{proto}://{domain}{path}"
                    
                    alternates_list.append({
                        'lang_code': lang_code,
                        'location': alt_loc
                    })
                    
                    if lang_code == 'en':
                        alternates_list.append({
                            'lang_code': 'x-default',
                            'location': alt_loc
                        })
                        
            url_info['alternates'] = alternates_list
            
        return urls


class ProductPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ProductPage.objects.live().public().select_related("product")

    def location(self, obj):
        return obj.url

    def lastmod(self, obj):
        return obj.product.updated_at if obj.product else obj.last_published_at

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        domain = site.domain if site else '127.0.0.1:8000'
        proto = protocol or 'http'
        
        for url_info in urls:
            obj = url_info.get('item')
            if not obj:
                continue

            alternates_list = []
            for locale in Locale.objects.all():
                try:
                    translation = obj.get_translation(locale)
                    if translation and translation.live:
                        alt_loc = f"{proto}://{domain}{translation.url}"
                        alternates_list.append({
                            'lang_code': locale.language_code,
                            'location': alt_loc
                        })
                        
                        if locale.language_code == 'en':
                            alternates_list.append({
                                'lang_code': 'x-default',
                                'location': alt_loc
                            })
                except Exception:
                    continue
            
            url_info['alternates'] = alternates_list
            
        return urls