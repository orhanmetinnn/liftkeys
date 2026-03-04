from django.urls import path
from . import views
from django.conf.urls import handler404
from .views import custom_404  # views.py'deki fonksiyonu import et
from .sitemaps import StaticViewSitemap, ProductPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
handler404 = custom_404
sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductPageSitemap,
}
urlpatterns = [
    path('employeecreate/', views.employee_manage_view, name='employee_create'),
    path('jobinfo/', views.jobinfo_view, name='jobinfo_edit'),
    path('api/employee/<int:employee_id>/', views.employee_detail_api, name='employee_detail_api'),
    path('report/employee/', views.report_employee, name='report_employee'),
    path('companies/manage/', views.company_manage_view, name='company_manage'),
    # Firma detay API'si (JSON döner)
    path('api/companies/<int:company_id>/', views.company_detail_api, name='company_detail_api'),
    path('api/sector/<int:sector_id>/', views.sector_detail_api, name='sector_detail_api'),
    # Country detay API
    path('api/country/<int:country_id>/', views.country_detail_api, name='country_detail_api'),
    path('directorycompany/update/', views.directory_company_update, name='directory_company_update'),
    path('catogory_detail_api/<int:category_id>/',views.catogory_detail_api,name='catogory_detail_api'),
    path('opportunity_detail/',views.OpportunityDetail, name='OpportunityDetail'),
    path('api/opportunity/<int:opportunity_id>/', views.opportunity_detail_api, name='opportunity_detail_api'),
    path("offers/create/", views.offer_create, name="offer_create"),
    path("get-products/<int:category_id>/", views.get_products_by_category, name="get_products_by_category"),
    path('offers/', views.offer_list, name='offer_list'),
    # path('offers/<int:offer_id>/pdf/', views.offer_pdf, name='offer_pdf'),
    path("",views.indexpage, name='indexpage'),
    path('categoriesmanage/', views.category_manage, name='category_manage'),
    path('categoriesmanage/<int:pk>/', views.category_manage, name='category_edit'),
    path('contact/', views.contactpage, name='contact'),
    path('crm/messages/', views.crm_contact_messages, name='crm_contact_messages'),
    path('crm/messages/toggle/<int:pk>/', views.crm_toggle_contacted, name='crm_toggle_contacted'),
    path('loginorcreate/',views.loginorcreate,name='loginorcreate'),
    path("product_hub/", views.product_hub, name="product_hub"),
    path("products/<int:product_id>/questions/", views.product_questions_view, name="product_questions"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_page, name="cart_page"),
    path("cart-summary-api/", views.cart_summary_api, name="cart_summary_api"),
    path("cart/update/", views.update_cart, name="update_cart"),  # miktar silme/düzenleme
    path("cart/checkout/", views.cart_checkout, name="cart_checkout"),  # iletişim formu
    path("kategori/", views.category_list, name="category_list"),
    path("kategori/<slug:slug>/", views.category_detail, name="category_detail"),
    path("contact-form/preview/", views.contact_form_view_preview, name="contact_form_view_preview"),
    path("about/", views.about_view, name="about"),

    path("privacy-policy/", views.privacy_view, name="gizlilikguvenlik"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/toggle/<int:pk>/", views.toggle_order_status, name="toggle_order_status"),
    path("404/", views.custom_404, name="test-404"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("gallery/", views.gallery_view, name="gallery_view"),
    path("api/gallery-items/", views.gallery_items_api, name="gallery_items_api"),  # ✅ yeni
    path("gallery/manager/", views.gallery_manager_view, name="gallery_manager"),
    path("gallery/manager/<int:item_id>/", views.gallery_manager_view, name="gallery_manager_edit"),

    path("safety-gear/", views.asansorfren_view, name="asansorfren_view"),

    path("atlas-overload/", views.atlas_overload_view, name="atlas_overload"),
    path("horus-photocell/", views.horusphotocell_view, name="horus_photocell"),
    path("switch-systems/", views.switchsystems_view, name="switch_systems"),
    path("zemin/", views.zemin_view, name="zemin_view"),
    path("fan/", views.fan_view, name="fan_view"),
    path("guideshoe/", views.paten_view, name="paten_view"),
    path("solid/", views.solid_view, name="solid_view"),
    path("kupeste/", views.kupeste_view, name="kupeste_view"),
    path("takozlar/", views.takozlar_view, name="takozlar_view"),
    path('keys/', views.anahtar_view, name='keys_view'),
    path('dekoratif-cam/', views.kabincam_view, name='kabincam_view'),
    path('patenkabin/', views.patenkabin_view, name='patenkabin_view'),


    path('feed/pinterest/', views.pinterest_catalog_feed, name='pinterest_feed'),
    path("kagittanisleri/", views.kagittanisler_view, name="kagittanisleri_view"),
    path(
        'robots.txt', 
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), 
        name="robots_file"
    ),
]





