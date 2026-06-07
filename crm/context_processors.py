from .models import Category, Product
from .forms import ContactForm
from django.db.models import Prefetch

def menu_context(request):
    # DÜZELTİLEN KISIM: Sadece '-created_at' yerine 'order', '-created_at' yazıyoruz.
    products_qs = Product.objects.filter(is_active=True).order_by('order', '-created_at').prefetch_related('market_images')

    categories = Category.objects.filter(
        menude_goster=True, 
        parent__isnull=True
    ).order_by('order', 'id').prefetch_related(
        'subcategories',
        # Featured products içine artık market resimleri de dahil edilmiş olacak
        Prefetch('product_set', queryset=products_qs, to_attr='featured_products')
    )
    
    return {"global_categories": categories}

def contact_form_context(request):
    return {
        "formiletisimpreview": ContactForm()
    }