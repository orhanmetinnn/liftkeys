from .models import Category, Product
from .forms import ContactForm
from .models import Category, Product
from django.db.models import Prefetch
def menu_context(request):
    # 1. İlişkili 'market_images' tablosunu da peşinen (prefetch) çekiyoruz.
    products_qs = Product.objects.filter(is_active=True).order_by('-created_at').prefetch_related('market_images')

    categories = Category.objects.filter(
        menude_goster=True, 
        parent__isnull=True
    ).prefetch_related(
        'subcategories',
        # Featured products içine artık market resimleri de dahil edilmiş olacak
        Prefetch('product_set', queryset=products_qs, to_attr='featured_products')
    )
    
    return {"global_categories": categories}



def contact_form_context(request):
    return {
        "formiletisimpreview": ContactForm()
    }




