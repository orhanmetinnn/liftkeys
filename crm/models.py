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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='title_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    name= models.CharField(max_length=250, verbose_name='Unvan Adı')

    def __str__(self):
            return self.name



class Department(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='department_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    name = models.CharField(max_length=250, verbose_name='Departman Adı')

    def __str__(self):
        return self.name
    

class WorkLocation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='work_location_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    name = models.CharField(max_length=250, verbose_name='Çalışma Lokasyonu Adı')

    def __str__(self):
        return self.name





class JobInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='job_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='job_info_as_employee')
    title = models.ForeignKey(TitlePersonel, on_delete=models.CASCADE, related_name='job_info', verbose_name='Unvan')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_info', verbose_name='Departman')

    manager = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='job_info_as_manager')
    
    
    employment_type = models.CharField(max_length=50, choices=[
        ("Full", "Tam Zamanlı"),
        ("Part", "Yarı Zamanlı"),
        ("Contract", "Sözleşmeli")
    ])
    work_location = models.ForeignKey(WorkLocation, on_delete=models.CASCADE, related_name='job_info', verbose_name='Çalışma Lokasyonu')



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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='country_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)  # ISO kod gibi

    def __str__(self):
        return self.name 

class Sector(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='sector_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    # Temel Bilgiler
    firma_adi = models.CharField(max_length=255)
    vergi_no = models.CharField(max_length=50, unique=True, verbose_name="Vergi Numarası / Kimlik Numarası")
    sektor = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    
    telefon = models.CharField(max_length=30, blank=True, null=True)
    telefon2 = models.CharField(max_length=30, blank=True, null=True, verbose_name="İkinci Telefon")
    fax = models.CharField(max_length=30, blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True, verbose_name="İkinci E-posta")
    
    websitesi = models.CharField(blank=True, null=True)
    
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
    linkedin = models.CharField(blank=True, null=True)
    twitter = models.CharField(blank=True, null=True)
    facebook = models.CharField(blank=True, null=True)
    instagram = models.CharField(blank=True, null=True)
    
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='directorycompany_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    companyselection=models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True,related_name="Firma_Secimi")
    first_name = models.CharField(verbose_name='Ad')
    last_name = models.CharField(verbose_name='Soyad')
    unvan=models.CharField(blank=True, null=True)
    telefon = models.CharField(blank=True, null=True)
    email=models.CharField(blank=True, null=True)
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







class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name







class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="Ürün Adı")
    website_image = models.ImageField(upload_to=product_website_image_path, blank=True, null=True, verbose_name="Web Sitesi Görseli")
    mobile_image = models.ImageField(upload_to=product_mobile_image_path, blank=True, null=True, verbose_name="Mobil Görünüm Görseli")
    features = models.TextField(blank=True, null=True, verbose_name="Ürün Özellikleri")
    stock_code = models.CharField(max_length=50, unique=True, verbose_name="Stok Kodu")
    categories = models.ManyToManyField(Category, blank=True, verbose_name="Kategoriler")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat", default=0.0)
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    warranty_period = models.CharField(max_length=50, blank=True, null=True, verbose_name="Garanti Süresi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name



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
    










