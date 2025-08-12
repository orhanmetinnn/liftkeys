from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad'}),
            'tc_identity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TC Kimlik No', 'maxlength': '11'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ornek@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05xx xxx xx xx'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user', 'cropping', 'cropping_free']  # Görünmesin istediklerin burada
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad'}),
            'tc_identity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TC Kimlik No', 'maxlength': '11'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ornek@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05xx xxx xx xx'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


from django import forms
from .models import JobInfo
from .models import TitlePersonel, Department, WorkLocation , Country, Sector



class JobInfoForm(forms.ModelForm):
    class Meta:
        model = JobInfo
        fields = [
            'user',
            'employee',
            'title',
            'department',
            'manager',
            'employment_type',
            'work_location',
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'work_location': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'İşlem Yapan Kullanıcı',
            'employee': 'Çalışan',
            'title': 'Unvan',
            'department': 'Departman',
            'manager': 'Yönetici',
            'employment_type': 'Çalışma Tipi',
            'work_location': 'Çalışma Lokasyonu',
        }





class TitlePersonelForm(forms.ModelForm):
    class Meta:
        model = TitlePersonel
        fields = ['user', 'name']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'İşlem Yapan Kullanıcı',
            'name': 'Unvan Adı',
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['user', 'name']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'İşlem Yapan Kullanıcı',
            'name': 'Departman Adı',
        }


class WorkLocationForm(forms.ModelForm):
    class Meta:
        model = WorkLocation
        fields = ['user', 'name']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'İşlem Yapan Kullanıcı',
            'name': 'Çalışma Lokasyonu Adı',
        }



from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'firma_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'vergi_no': forms.TextInput(attrs={'class': 'form-control'}),
            'sektor': forms.Select(attrs={'class': 'form-select'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon2': forms.TextInput(attrs={'class': 'form-control'}),
            'fax': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'email2': forms.EmailInput(attrs={'class': 'form-control'}),
            'websitesi': forms.URLInput(attrs={'class': 'form-control'}),
            'adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sehir': forms.TextInput(attrs={'class': 'form-control'}),
            'ilce': forms.TextInput(attrs={'class': 'form-control'}),
            'posta_kodu': forms.TextInput(attrs={'class': 'form-control'}),
            'ulke': forms.Select(attrs={'class': 'form-select'}),
            'kurulus_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'calisan_sayisi': forms.NumberInput(attrs={'class': 'form-control'}),
            'netciiro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sektor_alt_bilgisi': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_pozisyon': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'aktif_mi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notlar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'firma_adi': 'Firma Adı',
            'vergi_no': 'Vergi Numarası / Kimlik Numarası',
            'sektor': 'Sektör',
            'telefon': 'Telefon',
            'telefon2': 'İkinci Telefon',
            'fax': 'Fax',
            'email': 'E-posta',
            'email2': 'İkinci E-posta',
            'websitesi': 'Web Sitesi',
            'adres': 'Adres',
            'sehir': 'Şehir',
            'ilce': 'İlçe',
            'posta_kodu': 'Posta Kodu',
            'ulke': 'Ülke',
            'kurulus_tarihi': 'Kuruluş Tarihi',
            'calisan_sayisi': 'Çalışan Sayısı',
            'netciiro': 'Net Ciro',
            'sektor_alt_bilgisi': 'Sektör Alt Bilgisi',
            'yetkili_adi': 'Yetkili Adı',
            'yetkili_pozisyon': 'Yetkili Pozisyon',
            'yetkili_telefon': 'Yetkili Telefon',
            'yetkili_email': 'Yetkili E-posta',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'aktif_mi': 'Aktif mi?',
            'notlar': 'Notlar',
        }




class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['user']  
        widgets = {
            'firma_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'vergi_no': forms.TextInput(attrs={'class': 'form-control'}),
            'sektor': forms.Select(attrs={'class': 'form-select'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon2': forms.TextInput(attrs={'class': 'form-control'}),
            'fax': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'email2': forms.EmailInput(attrs={'class': 'form-control'}),
            'websitesi': forms.URLInput(attrs={'class': 'form-control'}),
            'adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sehir': forms.TextInput(attrs={'class': 'form-control'}),
            'ilce': forms.TextInput(attrs={'class': 'form-control'}),
            'posta_kodu': forms.TextInput(attrs={'class': 'form-control'}),
            'ulke': forms.Select(attrs={'class': 'form-select'}),
            'kurulus_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'calisan_sayisi': forms.NumberInput(attrs={'class': 'form-control'}),
            'netciiro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sektor_alt_bilgisi': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_pozisyon': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'yetkili_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'aktif_mi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notlar': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'firma_adi': 'Firma Adı',
            'vergi_no': 'Vergi Numarası / Kimlik Numarası',
            'sektor': 'Sektör',
            'telefon': 'Telefon',
            'telefon2': 'İkinci Telefon',
            'fax': 'Fax',
            'email': 'E-posta',
            'email2': 'İkinci E-posta',
            'websitesi': 'Web Sitesi',
            'adres': 'Adres',
            'sehir': 'Şehir',
            'ilce': 'İlçe',
            'posta_kodu': 'Posta Kodu',
            'ulke': 'Ülke',
            'kurulus_tarihi': 'Kuruluş Tarihi',
            'calisan_sayisi': 'Çalışan Sayısı',
            'netciiro': 'Net Ciro',
            'sektor_alt_bilgisi': 'Sektör Alt Bilgisi',
            'yetkili_adi': 'Yetkili Adı',
            'yetkili_pozisyon': 'Yetkili Pozisyon',
            'yetkili_telefon': 'Yetkili Telefon',
            'yetkili_email': 'Yetkili E-posta',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'aktif_mi': 'Aktif mi?',
            'notlar': 'Notlar',
        }






class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        exclude = ['user']  # Görünmesin istediklerin burada
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }




class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }



class UpdateSectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        exclude = ['user']  # Görünmesin istediklerin burada
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','id':'sector_name','name':'sector_name'}),
        }






from django import forms
from .models import DirectoryCompany

class DirectoryCompanyForm(forms.ModelForm):
    class Meta:
        model = DirectoryCompany
        fields = [
            'companyselection',
            'first_name',
            'last_name',
            'unvan',
            'telefon',
            'email',
            'notlar',
            'tarihselection',
            'iletisimnedeni',
            'bizi_nereden_buldu',  # yeni alan
        ]
        labels = {
            'companyselection': 'Firma Seçimi',
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'unvan': 'Ünvan / Görev',
            'telefon': 'Telefon',
            'email': 'E-posta',
            'notlar': 'Notlar',
            'tarihselection': 'Tarih Seçimi',
            'iletisimnedeni': 'İletişim Nedeni',
            'bizi_nereden_buldu': 'Bizi Nereden Buldu',
        }
        widgets = {
            'companyselection': forms.Select(attrs={'class': 'form-select','placeholder': 'Mevcut ise seçim yapınız'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad'}),
            'unvan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unvan / Görev'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'}),
            'iletisimnedeni': forms.Select(attrs={'class': 'form-select'}),
            'bizi_nereden_buldu': forms.Select(attrs={'class': 'form-select'}),
            'notlar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notlar'}),
            'tarihselection': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Modelde null=True ve blank=True olan alanlar formda zorunlu değil
        optional_fields = ['companyselection', 'unvan', 'telefon', 'email', 'notlar']
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False



from .models import Product, Option

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'website_image',
            'mobile_image',
            'offer_pdf',
            'features',
            'stock_code',
            'categories',
            'description',
            'price',
            'is_active',
            'warranty_period',
            'video_url',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'website_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'mobile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'offer_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock_code': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'warranty_period': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
        }




class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name', 'value', 'yayinla']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'yayinla': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }











# from django import forms
# from .models import Product, Category

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'website_image',
#             'mobile_image',
#             'offer_pdf',
#             'features',
#             'stock_code',
#             'categories',
#             'description',
#             'price',
#             'is_active',
#             'weight',
#             'dimensions',
#             'color',
#             'warranty_period',
#             'video_url',
#             'related_products',
#         ]
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ürün adı'}),
#             'website_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'mobile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'offer_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ürün özellikleri'}),
#             'stock_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stok kodu'}),
#             'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': True}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Açıklama'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
#             'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'En x Boy x Yükseklik'}),
#             'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Renk'}),
#             'warranty_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Garanti süresi'}),
#             'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Video URL'}),
#             'related_products': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': True}),
#         }
#         labels = {
#             'name': 'Ürün Adı',
#             'website_image': 'Web Sitesi Görseli',
#             'mobile_image': 'Mobil Görünüm Görseli',
#             'offer_pdf': 'Fiyat Teklifi PDF',
#             'features': 'Ürün Özellikleri',
#             'stock_code': 'Stok Kodu',
#             'categories': 'Kategoriler',
#             'description': 'Açıklama',
#             'price': 'Fiyat',
#             'is_active': 'Aktif Mi?',
#             'weight': 'Ağırlık (kg)',
#             'dimensions': 'Ölçüler (En x Boy x Yükseklik)',
#             'color': 'Renk',
#             'warranty_period': 'Garanti Süresi',
#             'video_url': 'Tanıtım Videosu URL',
#             'related_products': 'İlgili Ürünler',
#         }

