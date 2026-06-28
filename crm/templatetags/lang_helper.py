from django import template
from django.conf import settings
import re

register = template.Library()

# 2 harfli dil prefix'i: /en/, /ar/, /tr/ vb.
_LANG_PREFIX = re.compile(r'^/([a-z]{2})/')


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None):
    """
    Mevcut URL'nin dil prefix'ini değiştirerek hedef dile ait URL'yi döndürür.

    Örnekler:
      /en/solid/  + 'ar' → /ar/solid/
      /ar/solid/  + 'tr' → /solid/
      /solid/     + 'en' → /en/solid/
      /           + 'ar' → /ar/
      /en/en/     + 'ar' → /ar/   (recursive stripping — eski bug kalıntısı da düzeltilir)

    Wagtail veya translate_url'e bağımlı değil; her durumda çalışır ve çift prefix üretemez.
    """
    request = context.get('request')
    default_lang = settings.LANGUAGE_CODE  # 'tr'
    supported = {l[0] for l in settings.LANGUAGES}

    if not request:
        return '/' if lang == default_lang else f'/{lang}/'

    # Mevcut path'ten TÜM dil prefix'lerini recursive olarak soy.
    # Hem /tr/ (manuel route) hem /en/ /ar/ vb. prefix'lerini temizler.
    # Döngü: /en/en/solid/ → /en/solid/ → /solid/ → çıkış
    path = request.path
    while True:
        m = _LANG_PREFIX.match(path)
        if m and m.group(1) in supported:
            path = path[len(f'/{m.group(1)}'):]
        else:
            break

    # Hedef dil prefix'ini ekle (TR dahil tüm diller ön ek alır)
    return f'/{lang}{path}'