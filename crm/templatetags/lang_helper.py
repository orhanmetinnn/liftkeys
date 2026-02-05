from django import template
from django.urls import translate_url
from wagtail.models import Locale

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None):
    """
    Hem Wagtail sayfalarını hem de standart Django sayfalarını
    hedef dile çevirir.
    """
    request = context.get('request')
    page = context.get('page') # Wagtail, mevcut sayfayı context'e 'page' olarak koyar
    
    # 1. SENARYO: Eğer bu bir Wagtail Sayfası ise (Örn: Anasayfa, Hakkımızda, Ürünler)
    if page:
        try:
            # Hedef dilin Locale objesini bul (Örn: 'en', 'tr')
            target_locale = Locale.objects.get(language_code=lang)
            
            # Mevcut sayfanın o dildeki çevirisini bul
            translated_page = page.get_translation_or_none(target_locale)
            
            # Eğer çevirisi varsa ve yayındaysa onun URL'sini döndür
            if translated_page and translated_page.live:
                return translated_page.url
        except:
            # Bir hata olursa (dil bulunamazsa vs.) aşağıdaki standart yönteme geç
            pass

    # 2. SENARYO: Wagtail sayfası değilse (Örn: Arama sonuçları, Sepet, Admin paneli)
    # veya sayfanın çevirisi henüz oluşturulmamışsa standart Django çevirisi yap.
    try:
        if request:
            url = translate_url(request.path, lang)
            if url:
                return url
    except:
        pass

    # 3. SENARYO: Hiçbir şey çalışmazsa ana sayfaya at
    return f"/{lang}/"