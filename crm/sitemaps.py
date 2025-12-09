# urls.py ile aynı seviyede sitemaps.py aç
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from wagtail.models import Locale
from .models import ProductPage


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        # urls.py içinde name='indexpage', name='contact', name='about' olan path'ler
        return ['indexpage', 'contact', 'about']

    def location(self, item):
        return reverse(item)


# 🔹 Ürün Sayfaları (çok dilli ProductPage)
class ProductPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # sadece yayında olan ürün sayfaları
        return ProductPage.objects.live().public().select_related("product")

    def location(self, obj):
        return obj.url

    def lastmod(self, obj):
        # Ürün varsa ürün güncelleme tarihi, yoksa sayfanın publish tarihi
        return obj.product.updated_at if obj.product else obj.last_published_at

    def alternates(self, obj):
        """
        Her ürün sayfasının diğer dillerdeki URL’lerini çıkarır (hreflang).
        """
        alternates = []
        for locale in Locale.objects.all():
            try:
                translation = obj.get_translation(locale)
                if translation and translation.live:
                    alternates.append((locale.language_code, translation.url))
            except Exception:
                continue
        return alternates