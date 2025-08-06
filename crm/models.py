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


class JobInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='job_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='job_info')
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    employment_type = models.CharField(max_length=50, choices=[("Full", "Tam Zamanlı"), ("Part", "Yarı Zamanlı"), ("Contract", "Sözleşmeli")])
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    work_location = models.CharField(max_length=255)



class Education(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='education_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()




class Experience(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='experience_profile', verbose_name='İşlem Yapan Kullanıcı', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)











