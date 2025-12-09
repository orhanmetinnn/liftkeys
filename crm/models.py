from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin




class GeneralCustomBirim(models.Model):
    name = models.CharField(max_length=100, verbose_name='Genel Birim Adı')

    class Meta:
        verbose_name = 'Genel Birim'
        verbose_name_plural = 'Genel Birimler'

    def __str__(self):
        return self.name



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self.create_user(email, password, **extra_fields)


from image_cropping import ImageRatioField

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('customer', 'Customer'),   # yani ziyaretçi
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name='Rol',blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # cropping = ImageRatioField('profile_image', '300x300')  # Kırpma oranını burada belirleyin

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email 
    
    class Meta:
        verbose_name = 'Kullanıcı Bilgisi'
        verbose_name_plural = 'Kullanıcı Bilgileri'






class Employee(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employees',  # eski employee_profile yerine
        verbose_name='İşlem Yapan Kullanıcı',
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50,verbose_name='Ad')
    last_name = models.CharField(max_length=50,verbose_name='Soyad')
    tc_identity = models.CharField(max_length=11, unique=True,verbose_name='TC Kimlik No')
    birth_date = models.DateField(verbose_name='Doğum Tarihi')
    gender = models.CharField(max_length=10, choices=[("M", "Erkek"), ("F", "Kadın")],verbose_name='Cinsiyet')
    email = models.EmailField(verbose_name='E-posta', unique=True)
    phone = models.CharField(max_length=20,verbose_name='Telefon Numarası', blank=True, null=True)
    address = models.TextField(blank=True, null=True,verbose_name='Adres')
    start_date = models.DateField(verbose_name='İşe Başlama Tarihi', null=True, blank=True)
    profile_image = models.ImageField(upload_to='employee_images/', blank=True, null=True,verbose_name='Profil Resmi')
    cropping = ImageRatioField('profile_image', '300x300')  # Kırpma oranını burada belirleyin
    is_active = models.BooleanField(default=True,verbose_name='Aktif Mi?')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.tc_identity})"





class TitlePersonel(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='titles',
        verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True
    )
    name = models.CharField(max_length=250, verbose_name='Unvan Adı')

    def __str__(self):
        return self.name


class Department(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='departments',
        verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True
    )
    name = models.CharField(max_length=250, verbose_name='Departman Adı')

    def __str__(self):
        return self.name

    

class WorkLocation(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='work_locations',
        verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True
    )
    name = models.CharField(max_length=250, verbose_name='Çalışma Lokasyonu Adı')

    def __str__(self):
        return self.name






class JobInfo(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='job_profiles',
        verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='job_infos', verbose_name='Çalışan')
    title = models.ForeignKey(TitlePersonel, on_delete=models.CASCADE, related_name='job_info', verbose_name='Unvan')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_info', verbose_name='Departman')
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='managed_jobs', verbose_name='Yönetici')
    employment_type = models.CharField(max_length=50, choices=[
        ("Full", "Tam Zamanlı"),
        ("Part", "Yarı Zamanlı"),
        ("Contract", "Sözleşmeli")
    ])
    work_location = models.ForeignKey(WorkLocation, on_delete=models.CASCADE, related_name='job_info', verbose_name='Çalışma Lokasyonu')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.title}"

    
    


class Education(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='education_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=255,null=True, blank=True,verbose_name='Okul Adı')
    degree = models.CharField(max_length=100, null=True, blank=True,verbose_name='Derece')
    field_of_study = models.CharField(max_length=100, null=True, blank=True,verbose_name='Bölüm')
    start_date = models.DateField(verbose_name="Başlangıç Tarihi", null=True, blank=True)
    end_date = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)




class Experience(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='experience_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)












from django.db import models

class Country(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='countries',
        verbose_name='İşlem Yapan Kullanıcı',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)  # ISO kod gibi

    def __str__(self):
        return self.name 

class Sector(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='sectors',
        verbose_name='İşlem Yapan Kullanıcı',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='companies',
        verbose_name='İşlem Yapan Kullanıcı',
        null=True,
        blank=True
    )
    # Temel Bilgiler
    firma_adi = models.CharField(max_length=255)
    vergi_no = models.CharField(max_length=50, unique=True, verbose_name="Vergi Numarası / Kimlik Numarası")
    sektor = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    
    telefon = models.CharField(max_length=30, blank=True, null=True)
    telefon2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="İkinci Telefon")
    fax = models.CharField(max_length=30, blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True, verbose_name="İkinci E-posta")
    
    websitesi = models.CharField(max_length=255,blank=True, null=True)
    
    adres = models.TextField(blank=True, null=True)
    sehir = models.CharField(max_length=100, blank=True, null=True)
    ilce = models.CharField(max_length=100, blank=True, null=True)
    posta_kodu = models.CharField(max_length=20, blank=True, null=True)
    ulke = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Ek Bilgiler
    kurulus_tarihi = models.DateField(blank=True, null=True)
    calisan_sayisi = models.PositiveIntegerField(blank=True, null=True)
    netciiro = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Net Ciro")
    sektor_alt_bilgisi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sektör Alt Bilgisi")
    
    # Yetkili Kişi Bilgileri
    yetkili_adi = models.CharField(max_length=255, blank=True, null=True)
    yetkili_pozisyon = models.CharField(max_length=255, blank=True, null=True)
    yetkili_telefon = models.CharField(max_length=30, blank=True, null=True)
    yetkili_email = models.EmailField(blank=True, null=True)
    
    # Sosyal Medya Hesapları
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    
    # Durum ve Notlar
    aktif_mi = models.BooleanField(default=True)
    notlar = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.firma_adi






    
class DirectoryCompany(models.Model):
    ILETISIM_NEDENLERI = [
        ('teklif', 'Teklif Talebi'),
        ('destek', 'Destek Talebi'),
        ('bilgi', 'Bilgi İsteme'),
        ('is_ortakligi', 'İş Ortaklığı Talebi'),
        ('satis', 'Satış Temsilcisi Görüşmesi'),
        ('teknik', 'Teknik Destek'),
        ('musteri_hizmetleri', 'Müşteri Hizmetleri İletişimi'),
        ('odeme', 'Ödeme / Faturalandırma'),
        ('toplanti', 'Toplantı / Randevu Talebi'),
        ('referans', 'Referans / Tavsiye İsteği'),
        ('pazarlama', 'Pazarlama / Tanıtım Talebi'),
        ('diger', 'Diğer'),
    ]

    BIZI_NEREDEN_BULDU = [
        ('bizulastik','Biz Ulaştık'),
        ('arama_motorlari', 'Arama Motorları'),
        ('internet', 'İnternet / Arama Motorları'),
        ('sosyal_medya', 'Sosyal Medya'),
        ('arkadas_tavsiye', 'Arkadaş / Tavsiye'),
        ('reklam', 'Reklam'),
        ('fuar', 'Fuar / Etkinlik'),
        ('diger', 'Diğer'),
    ]
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='directory_companies',
        verbose_name='İşlem Yapan Kullanıcı',
        null=True,
        blank=True
    )
    companyselection=models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,related_name="Firma_Secimi")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    unvan = models.CharField(max_length=255, blank=True, null=True)
    telefon = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    notlar=models.TextField(blank=True, null=True)
    tarihselection=models.DateField(verbose_name='Tarih Seçimi',null=True, blank=True)
    iletisimnedeni = models.CharField(
        max_length=50,
        choices=ILETISIM_NEDENLERI,
        blank=True,
        null=True,
        verbose_name="İletişim Nedeni"
    )

    bizi_nereden_buldu = models.CharField(
        max_length=50,
        choices=BIZI_NEREDEN_BULDU,
        blank=True,
        null=True,
        verbose_name="Bizi Nereden Buldu"
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)  # Oluşturulma tarihi (sadece ilk kayıtta set edilir)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True) 





from django.db import models

def product_website_image_path(instance, filename):
    return f"products/{instance.id}/website/{filename}"

def product_mobile_image_path(instance, filename):
    return f"products/{instance.id}/mobile/{filename}"

def product_offer_pdf_path(instance, filename):
    return f"products/{instance.id}/offers/{filename}"





from django.utils.text import slugify
class Category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kullanıcı")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True, verbose_name="Slug")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="Üst Kategori"
    )
    menude_goster = models.BooleanField(default=True, verbose_name="Menüde Göster", blank=True, null=True)
    menu_image = models.ImageField(upload_to='category_menu_images/', blank=True, null=True, verbose_name="Menü Görseli")
    ust_menu_image = models.ImageField(upload_to='category_menu_images/', blank=True, null=True, verbose_name="Üst Menü Görseli")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Güncellenme Tarihi")

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        name_display = self.name or self.name_tr or self.name_en or "(İsimsiz)"
        if self.parent:
            return f"{self.parent} > {name_display}"
        return name_display


from django.utils.translation import get_language
from django.apps import apps
from django.urls import reverse
from wagtail.models import Page
from django.utils.translation import get_language, get_language_from_path
from wagtail.models import Locale

class Product(models.Model):
    CURRENCY_CHOICES = [
        ('TRY', 'TRY'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('SAR', 'SAR'),
        ('AED', 'AED'),
        ('EGP', 'EGP'),
        ('QAR', 'QAR'),
        ('KWD', 'KWD'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="İşlem Yapan Kullanıcı"
    )

    name = models.CharField(max_length=250, verbose_name="Ürün Adı")
    website_image = models.ImageField(upload_to="product_website_images/", blank=True, null=True, verbose_name="Web Sitesi Görseli")
    mobile_image = models.ImageField(upload_to="product_mobile_images/", blank=True, null=True, verbose_name="Mobil Görünüm Görseli")
    product_category_image = models.ImageField(upload_to="product_category_images/", blank=True, null=True, verbose_name="Kategori Görseli")

    features = models.TextField(blank=True, null=True, verbose_name="Ürün Özellikleri")
    stock_code = models.CharField(max_length=50, unique=True, verbose_name="Stok Kodu")
    categories = models.ManyToManyField("Category", blank=True, verbose_name="Kategoriler")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")

    price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Fiyat", default=0.0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD', verbose_name="Para Cinsi", blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    warranty_period = models.CharField(max_length=50, blank=True, null=True, verbose_name="Garanti Süresi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self, request=None, language_code=None):
        from crm.models import ProductPage
        qs = ProductPage.objects.filter(product=self)

        print("DEBUG >>> Product:", self.name)
        print("DEBUG >>> All Pages:", qs.values("id", "title", "locale__language_code"))

        if language_code:
            lang = language_code.split('-')[0]
        elif request and hasattr(request, 'LANGUAGE_CODE'):
            lang = (request.LANGUAGE_CODE or 'tr').split('-')[0]
        else:
            from django.utils.translation import get_language
            lang = (get_language() or 'tr').split('-')[0]

        print("DEBUG >>> Selected lang:", lang)

        page = qs.filter(locale__language_code=lang).first()
        print("DEBUG >>> Found page:", page)

        if not page:
            page = qs.filter(locale__language_code='tr').first()
            print("DEBUG >>> Fallback page:", page)

        if not page:
            return "#"

        return page.get_url(request=request) if request else page.url



class ProductMarketImage(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_market_images",
        verbose_name="İşlem Yapan Kullanıcı"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="market_images")
    image = models.ImageField(upload_to="product_market_images/")
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Alternatif Metin")

    def __str__(self):
        return f"{self.product.name} - {self.alt_text or 'Market Görseli'}"






class ProductQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("radio", "Tek Seçim (Radio)"),
        ("checkbox", "Çoklu Seçim (Checkbox)"),
        ("button", "Buton Grubu"),
        ("text", "Serbest Metin"),
    ]
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_questions",
        verbose_name="İşlem Yapan Kullanıcı"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default="text")

    def __str__(self):
        return f"{self.product.name} → {self.question_text}"


class ProductQuestionOption(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_question_options",
        verbose_name="İşlem Yapan Kullanıcı"
    )
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text
    
    
from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model

class ProductAnswer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="answers",blank=True, null=True)
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, related_name="answers",blank=True, null=True)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=50, blank=True, null=True)  # login olmayanlar için
    answer_text = models.TextField(verbose_name="Cevap",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} | {self.question.question_text[:20]} → {self.answer_text[:30]}"




from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks


from wagtail.models import Page

class SiteRoot(Page):
    """Sadece kapsayıcı. İçerik alanı yok."""
    # Root altında açılabilir
    parent_page_types = ['wagtailcore.Page']  # root'ta görünecek
    # Altına HomePage ve diğer dillerdeki Home sayfaları açabilsin
    subpage_types = [
        'crm.HomePage',         # mevcut HomePage
        'crm.BlogIndexPage',   # blog index
    ]

    class Meta:
        verbose_name = "Site Root"
        verbose_name_plural = "Site Root"


class HomePage(Page):
    template = "preview/index.html"
    parent_page_types = ['crm.SiteRoot']  # HomePage yalnızca SiteRoot altında açılabilsin
    subpage_types = ['crm.ProductPage','crm.BlogIndexPage']   # Altına ProductPage gibi sayfalar açabilsin

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Home page"
        verbose_name_plural = "Home pages"

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel 
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock  # burayı ekledik
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock  # Embed için ekledik
from .models import Product
from wagtail.contrib.table_block.blocks import TableBlock
class ProductPage(Page):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Bağlı Ürün"
    )

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", label="Başlık")),
        ('paragraph', blocks.RichTextBlock(label="Paragraf")),
        ('image', ImageChooserBlock(label="Resim")),
        ('video', blocks.URLBlock(label="Video URL")),
        ('list', blocks.ListBlock(blocks.CharBlock(), label="Liste")),
        ('quote', blocks.BlockQuoteBlock(label="Alıntı")),
        ('html', blocks.RawHTMLBlock(label="HTML")),
        ('embed', EmbedBlock(label="Embed")),
        ('page', blocks.PageChooserBlock(label="Sayfa Seç")),
        ('table', TableBlock(label="Tablo")),
        ('feature', blocks.StructBlock([
            ('title', blocks.CharBlock(label="Özellik Başlığı")),
            ('description', blocks.RichTextBlock(label="Özellik Açıklaması")),
            ('image', ImageChooserBlock(required=False, label="Özellik Resmi")),
        ], label="Özellik")),
        ('faq', blocks.ListBlock(
            blocks.StructBlock([
                ('question', blocks.CharBlock(label="Soru")),
                ('answer', blocks.RichTextBlock(label="Cevap")),
            ]),
            label="Sık Sorulan Sorular"
        )),
    ], blank=True)  # ✅ use_json_field bırakılabilir (3.x destekler)

    content_panels = Page.content_panels + [
        FieldPanel('product'),
        FieldPanel('body'),  # ✅ StreamFieldPanel kaldırıldı
    ]

    template = "productmanager/product_page.html"


    class Meta:
        verbose_name = "Ürün Sayfası"
        verbose_name_plural = "Ürün Sayfaları"

    def save(self, *args, **kwargs):
        """
        Sayfa kaydedilirken ürün adı slug olarak atanır (eğer elle değiştirilmemişse).
        """
        if self.product and not self.slug:
            self.slug = slugify(self.product.name)
        super().save(*args, **kwargs)

    def get_context(self, request):
        context = super().get_context(request)
        if self.product:
            context["product"] = self.product
            context["questions"] = (
                self.product.questions.prefetch_related("options").all()
            )
        else:
            context["questions"] = []
        return context


from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel



# ✅ Blog Index Page (liste sayfası)
class BlogIndexPage(Page):
    intro = models.TextField(blank=True, verbose_name="Açıklama")

    # Sadece BlogPage eklenebilsin
    subpage_types = ["crm.BlogPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    template = "blog/blog_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        # Bu index altındaki tüm BlogPage'leri getir
        context['posts'] = BlogPage.objects.live().descendant_of(self).order_by('-first_published_at')
        return context


# ✅ Blog Page (detay sayfası)
class BlogPage(Page):
    subtitle = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Alt Başlık"
    )

    # ✅ Kapak görseli (isteğe bağlı)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Kapak Görseli"
    )

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", label="Başlık")),
        ('paragraph', blocks.RichTextBlock(label="Paragraf")),
        ('image', ImageChooserBlock(label="Resim")),
        ('video', blocks.URLBlock(label="Video URL")),
        ('list', blocks.ListBlock(blocks.CharBlock(), label="Liste")),
        ('quote', blocks.BlockQuoteBlock(label="Alıntı")),
        ('html', blocks.RawHTMLBlock(label="HTML")),
        ('embed', EmbedBlock(label="Embed")),
        ('table', TableBlock(label="Tablo")),
    ], use_json_field=True, blank=True)

    date = models.DateField("Yayın Tarihi", auto_now_add=True)

    parent_page_types = ["crm.BlogIndexPage"]

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("featured_image"),  # ✅ kapak görseli paneli
        FieldPanel("body"),
        # FieldPanel("date"),
    ]

    template = "blog/blog_page.html"

    class Meta:
        verbose_name = "Blog Yazısı"
        verbose_name_plural = "Blog Yazıları"

class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=250, verbose_name="Özellik Adı")  # Ör: "Cam", "Renk", "Ağırlık"
    value = models.CharField(max_length=250, verbose_name="Değer")       # Ör: "Şeffaf", "Kırmızı", "12 kg"
    yayinla=models.BooleanField(default=True, verbose_name="Yayınla")
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"











# Fırsat Durumları
OPPORTUNITY_STATUS_CHOICES = [
    ('new', 'Yeni'),
    ('in_progress', 'İşlemde'),
    ('won', 'Kazanıldı'),
    ('lost', 'Kaybedildi'),
]

# Öncelik Seviyesi
PRIORITY_CHOICES = [
    ('low', 'Düşük'),
    ('medium', 'Orta'),
    ('high', 'Yüksek'),
]

OPPORTUNITY_STATUS_CHOICES = [
    ('new', 'Yeni'),
    ('in_progress', 'İşlemde'),
    ('won', 'Kazanıldı'),
    ('lost', 'Kaybedildi'),
]

# Öncelik Seviyesi
PRIORITY_CHOICES = [
    ('low', 'Düşük'),
    ('medium', 'Orta'),
    ('high', 'Yüksek'),
]

# Fırsat Kaynağı
LEAD_SOURCE_CHOICES = [
    ('referral', 'Referans'),
    ('website', 'Web Sitesi'),
    ('fair', 'Fuar'),
    ('social_media', 'Sosyal Medya'),
    ('other', 'Diğer'),
]

class Opportunity(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunities',
        verbose_name="İşlem Yapan Kullanıcı"
    )
    name = models.CharField(max_length=250, verbose_name="Fırsat Adı")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name="Firma")
    products = models.ManyToManyField('Product', blank=True, verbose_name="Ürünler")  # Birden fazla ürün seçilebilir
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama / Notlar")
    status = models.CharField(max_length=20, choices=OPPORTUNITY_STATUS_CHOICES, default='new', verbose_name="Durum")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Öncelik")
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Tahmini Değer")
    expected_close_date = models.DateField(blank=True, null=True, verbose_name="Tahmini Kapanış Tarihi")
    lead_source = models.CharField(max_length=50, choices=LEAD_SOURCE_CHOICES, blank=True, null=True, verbose_name="Fırsatın Kaynağı")
    owner = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sorumlu Çalışan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.company.firma_adi}"
    


class Offer(models.Model):
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name="Fırsat"
    )
    banner_image = models.ImageField(
        upload_to='offer_banners/',
        verbose_name="Banner Görseli",
        blank=True,
        null=True
    )
    company_name = models.CharField(max_length=255, verbose_name="Teklif gönderen firma Adı")
    offer_date = models.DateField(auto_now_add=True, verbose_name="Teklif Tarihi")
    company_address = models.TextField(verbose_name="Firma Adresi")
    company_phone = models.CharField(max_length=30, verbose_name="Firma Telefonu")
    company_email = models.EmailField(verbose_name="Firma E-posta")
    company_website = models.CharField(max_length=255,verbose_name="Firma Web Sitesi")
    contact_person = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="İlgili Kişi"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    products = models.ManyToManyField(
        Product,
        through="OfferProduct",   # 👈 burası önemli
        related_name='offers',
        verbose_name="Ürünler"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.opportunity.name} - Teklif {self.offer_date}"


class OfferProduct(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Adet")
    # Ekstra alanlar
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        verbose_name="İndirim (%)"
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name="İnen Tutar"
    )
    final_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name="Son Fiyat"
    )
    def save(self, *args, **kwargs):
        if self.product.price:
            # İndirimli tutar
            if self.discount_percentage:
                self.discount_amount = (self.product.price * self.quantity * self.discount_percentage) / 100
            elif self.discount_amount:
                self.discount_amount = self.discount_amount * self.quantity  # toplam indirim
            else:
                self.discount_amount = 0
            
            # Son fiyat (adetli)
            self.final_price = (self.product.price * self.quantity) - self.discount_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.offer} - {self.product.name}"








class ContactMessage(models.Model):
    name = models.CharField("Ad", max_length=100)
    email = models.EmailField("E-posta")
    subject = models.CharField("Konu", max_length=200, blank=True)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    message = models.TextField("Mesaj")
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField("İletişime Geçildi", default=False,blank=True,null=True)  # Yeni alan

    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"










class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name="İşlem Yapan Kullanıcı"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="İşleme Geçildi mi?", blank=True, null=True)


    def __str__(self):
        return f"Sipariş #{self.id} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=1)
    answers = models.JSONField(default=dict, blank=True)  # Sorular JSON formatında saklanacak

    def __str__(self):
        return f"{self.product} x {self.qty}"
    


LANGUAGES = [
    ('tr', 'Turkish'),
    ('en', 'English'),
    ('ar', 'Arabic'),
    ('ru', 'Russian'),
    ('fr', 'Français'),
    ('de', 'German'),
]

class GalleryItem(models.Model):
    CONTENT_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    content_type = models.CharField(max_length=10, choices=CONTENT_CHOICES)
    image = models.ImageField(upload_to="gallery/images/", blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    youtube_thumbnail = models.URLField(blank=True, null=True)  # yeni alan
    created_at = models.DateTimeField(auto_now_add=True)

    # Çoklu dil title alanları
    title_tr = models.CharField(max_length=200, blank=True, null=True)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_ar = models.CharField(max_length=200, blank=True, null=True)
    title_ru = models.CharField(max_length=200, blank=True, null=True)
    title_fr = models.CharField(max_length=200, blank=True, null=True)
    title_de = models.CharField(max_length=200, blank=True, null=True)

    def youtube_embed(self):
        if self.youtube_url:
            return self.youtube_url.replace("watch?v=", "embed/").replace("&", "?")
        return None

    def __str__(self):
        return self.title_tr or "Gallery Item"