from django import forms
from .models import Employee


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


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
from .models import TitlePersonel, Department, WorkLocation , Country, Sector,Category,ProductMarketImage
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

from django import forms
from .models import DirectoryCompany,Product,Option

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



from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .models import Product, Category

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label=_("Kategoriler"),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6})
    )

    class Meta:
        model = Product
        fields = [
            # Çok dilli alanlar
            "name_tr", "name_en", "name_ar", "name_fr", "name_de", "name_ru",
            "features_tr", "features_en", "features_ar", "features_fr", "features_de", "features_ru",
            "description_tr", "description_en", "description_ar", "description_fr", "description_de", "description_ru",
            "warranty_period_tr", "warranty_period_en", "warranty_period_ar", "warranty_period_fr", "warranty_period_de", "warranty_period_ru",
            
            # Tek dilli alanlar
            "stock_code", "price", "currency", 
            "order", # YENİ EKLENEN: Sıralama alanı
            "website_image", "mobile_image", "product_category_image",
            "categories", "is_active",
        ]
        widgets = {
            # Çok dilli alanlar
            "name_tr": forms.TextInput(attrs={"class": "form-control"}),
            "name_en": forms.TextInput(attrs={"class": "form-control"}),
            "name_ar": forms.TextInput(attrs={"class": "form-control"}),
            "name_fr": forms.TextInput(attrs={"class": "form-control"}),
            "name_de": forms.TextInput(attrs={"class": "form-control"}),
            "name_ru": forms.TextInput(attrs={"class": "form-control"}),

            "features_tr": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "features_en": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "features_ar": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "features_fr": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "features_de": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "features_ru": forms.Textarea(attrs={"class": "form-control", "rows": 4}),

            "description_tr": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "description_en": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "description_ar": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "description_fr": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "description_de": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "description_ru": forms.Textarea(attrs={"class": "form-control", "rows": 4}),

            "warranty_period_tr": forms.TextInput(attrs={"class": "form-control"}),
            "warranty_period_en": forms.TextInput(attrs={"class": "form-control"}),
            "warranty_period_ar": forms.TextInput(attrs={"class": "form-control"}),
            "warranty_period_fr": forms.TextInput(attrs={"class": "form-control"}),
            "warranty_period_de": forms.TextInput(attrs={"class": "form-control"}),
            "warranty_period_ru": forms.TextInput(attrs={"class": "form-control"}),

            # Tek dilli alanlar
            "stock_code": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            
            # YENİ EKLENEN: Sıralama widget'ı (Negatif değer girilmesini engeller)
            "order": forms.NumberInput(attrs={"class": "form-control", "min": "0", "placeholder": "Menü Sırası (Örn: 1)"}),
            
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "website_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "mobile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "product_category_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Her dil için placeholder set et
        lang_placeholders = {
            "tr": {
                "name_tr": "Ürün Adı",
                "features_tr": "Ürün özellikleri",
                "description_tr": "Açıklama",
                "warranty_period_tr": "Örn: 24 Ay",
            },
            # ... diğer diller aynı kalıyor ...
        }

        for lang, fields in lang_placeholders.items():
            for field, placeholder in fields.items():
                if field in self.fields:
                    self.fields[field].widget.attrs.update({"placeholder": placeholder})

    def save(self, commit=True):
        # 1. Instance oluşturulur (DB'ye yazılmaz)
        instance = super(ProductForm, self).save(commit=False)

        # 2. Ana 'name' alanı boşsa, Türkçe (veya diğer) dilden doldurulur
        if not instance.name:
            instance.name = instance.name_tr or instance.name_en or "Ürün"

        if commit:
            instance.save()
            # 3. Many-to-Many ilişkiler (Kategoriler) kaydedilir
            self.save_m2m()

        return instance

class ProductMarketImageForm(forms.ModelForm):
    class Meta:
        model = ProductMarketImage
        fields = ["image", "alt_text", "order"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "alt_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Alternatif metin (SEO)"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Sıralama (Örn: 0, 1, 2)", "min": "0"}),
        }
        labels = {
            "image": "Market Görseli",
            "alt_text": "Alternatif Metin",
            "order": "Sıralama",
        }

ProductMarketImageFormSet = inlineformset_factory(
    parent_model=Product,
    model=ProductMarketImage,
    form=ProductMarketImageForm,
    extra=0,            # yeni kayıt için boş satır
    can_delete=True,    # mevcut görselleri silebil
)



from .models import Product, ProductMarketImage, ProductQuestion, ProductQuestionOption


class ProductQuestionForm(forms.ModelForm):
    class Meta:
        model = ProductQuestion
        # Çok dilli alanları dahil ettik:
        fields = [
            "question_text_tr", "question_text_en", "question_text_ar",
            "question_text_fr", "question_text_de", "question_text_ru",
            "question_type"
        ]
        widgets = {
            "question_text_tr": forms.TextInput(attrs={"class": "form-control"}),
            "question_text_en": forms.TextInput(attrs={"class": "form-control"}),
            "question_text_ar": forms.TextInput(attrs={"class": "form-control"}),
            "question_text_fr": forms.TextInput(attrs={"class": "form-control"}),
            "question_text_de": forms.TextInput(attrs={"class": "form-control"}),
            "question_text_ru": forms.TextInput(attrs={"class": "form-control"}),

            "question_type": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "tr": "Soruyu buraya yazın...",
            "en": "Write the question here...",
            "ar": "اكتب السؤال هنا...",
            "fr": "Écrivez la question ici...",
            "de": "Frage hier eingeben...",
            "ru": "Введите вопрос здесь...",
        }

        # Placeholderları dil alanlarına tek tek uygula
        for lang_code, placeholder in placeholders.items():
            field_name = f"question_text_{lang_code}"
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({"placeholder": placeholder})


class ProductQuestionOptionForm(forms.ModelForm):
    class Meta:
        model = ProductQuestionOption
        fields = [
            "option_text_tr", "option_text_en", "option_text_ar",
            "option_text_fr", "option_text_de", "option_text_ru"
        ]
        widgets = {
            "option_text_tr": forms.TextInput(attrs={"class": "form-control"}),
            "option_text_en": forms.TextInput(attrs={"class": "form-control"}),
            "option_text_ar": forms.TextInput(attrs={"class": "form-control"}),
            "option_text_fr": forms.TextInput(attrs={"class": "form-control"}),
            "option_text_de": forms.TextInput(attrs={"class": "form-control"}),
            "option_text_ru": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "tr": "Şık metni giriniz",
            "en": "Enter option text",
            "ar": "أدخل نص الخيار",
            "fr": "Entrez le texte de l'option",
            "de": "Optionstext eingeben",
            "ru": "Введите вариант ответа",
        }

        for lang_code, placeholder in placeholders.items():
            field_name = f"option_text_{lang_code}"
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({"placeholder": placeholder})


# Formset'leri aynı tutuyoruz, çünkü instance hangi Product / Question'a bağlıysa 
# dil alanları da otomatik geliyor.
ProductQuestionFormSet = inlineformset_factory(
    Product,
    ProductQuestion,
    form=ProductQuestionForm,
    extra=0,
    can_delete=True,
    validate_max=True
)

ProductQuestionOptionFormSet = inlineformset_factory(
    ProductQuestion,
    ProductQuestionOption,
    form=ProductQuestionOptionForm,
    extra=0,
    can_delete=True
)





class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name', 'value', 'yayinla']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'yayinla': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name_tr', 'name_en', 'name_ar', 'name_ru', 'name_fr', 'name_de',
            'parent', 'menude_goster', 'order', 'menu_image', 'ust_menu_image' # 'order' eklendi
        ]
        widgets = {
            'name_tr': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategori adı (Türkçe)'
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name (English)'
            }),
            'name_ar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الفئة (العربية)'
            }),
            'name_ru': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя категории (Русский)'
            }),
            'name_fr': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de catégorie (Français)'
            }),
            'name_de': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoriename (Deutsch)'
            }),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'menude_goster': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # YENİ EKLENEN: Sıralama alanı için numara giriş widget'ı
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0', # Negatif sayı girilmesini HTML tarafında da engeller
                'placeholder': 'Örn: 1 (Küçük sayı önce gösterilir)'
            }),
            
            'menu_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ust_menu_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name_tr': 'Kategori Adı (TR)',
            'name_en': 'Kategori Adı (EN)',
            'name_ar': 'Kategori Adı (AR)',
            'name_ru': 'Kategori Adı (RU)',
            'name_fr': 'Kategori Adı (FR)',
            'name_de': 'Kategori Adı (DE)',
            'parent': 'Üst Kategori',
            'menude_goster': 'Menüde Göster',
            
            # YENİ EKLENEN: Etiket
            'order': 'Menü Sırası',
            
            'menu_image': 'Menü Görseli',
            'ust_menu_image': 'Üst Menü Görseli'
        }

    def save(self, commit=True):
        # Formdan gelen veriyi al ama veritabanına henüz yazma
        instance = super(CategoryForm, self).save(commit=False)

        # Eğer ana 'name' alanı boşsa, uygun dili ata
        if not instance.name:
            instance.name = getattr(instance, 'name_tr', None) or getattr(instance, 'name_en', None) or "Kategori"
        
        # Eğer commit True ise (doğrudan kaydediliyorsa) veritabanına yaz
        if commit:
            instance.save()
            
        # DİKKAT: Bu satır 'if commit:' ile aynı hizada (girintide) olmalıdır!
        # İçeride kalırsa commit=False olduğunda None döner ve hata alırsın.
        return instance

        
from .models import Opportunity
class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            'name', 'company', 'products', 'description', 'status', 'priority',
            'estimated_value', 'expected_close_date', 'lead_source', 'owner'
        ]
        labels = {
            'name': 'Fırsat Adı',
            'company': 'Firma',
            'products': 'Ürünler',
            'description': 'Açıklama / Notlar',
            'status': 'Durum',
            'priority': 'Öncelik',
            'estimated_value': 'Tahmini Değer',
            'expected_close_date': 'Tahmini Kapanış Tarihi',
            'lead_source': 'Fırsatın Kaynağı',
            'owner': 'Sorumlu Çalışan',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'products': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expected_close_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lead_source': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
        }






class UpdateOpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            'name', 'company', 'products', 'description', 'status', 'priority',
            'estimated_value', 'expected_close_date', 'lead_source', 'owner'
        ]
        labels = {
            'name': 'Fırsat Adı',
            'company': 'Firma',
            'products': 'Ürünler',
            'description': 'Açıklama / Notlar',
            'status': 'Durum',
            'priority': 'Öncelik',
            'estimated_value': 'Tahmini Değer',
            'expected_close_date': 'Tahmini Kapanış Tarihi',
            'lead_source': 'Fırsatın Kaynağı',
            'owner': 'Sorumlu Çalışan',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'products': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expected_close_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lead_source': forms.Select(attrs={'class': 'form-select'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
        }






from .models import Offer
from django.forms import inlineformset_factory
from .models import Offer, OfferProduct
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'opportunity',
            'banner_image',
            'company_name',
            'company_address',
            'company_phone',
            'company_email',
            'company_website',
            'contact_person',
            'notes',
        ]
        widgets = {
            'opportunity': forms.Select(attrs={'class': 'form-select'}),
            'banner_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_website': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class OfferProductForm(forms.ModelForm):
    class Meta:
        model = OfferProduct
        fields = [
            'product',
            'quantity',
            'discount_percentage',
            'discount_amount',
            'final_price',
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'final_price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        }


OfferProductFormSet = inlineformset_factory(
    Offer,
    OfferProduct,
    form=OfferProductForm,
    extra=1,       # Başlangıçta 1 satır göster
    can_delete=True
)













from django import forms
from .models import ContactMessage
from django import forms
from .models import ContactMessage
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.ModelForm):
    # HONEYPOT ALANI: Kullanıcılar görmez, botlar doldurur.
    website_url = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'style': 'display: none;', # CSS ile gizliyoruz
            'autocomplete': 'off',
            'tabindex': '-1' # Klavyeyle form dolduranlar buraya takılmasın diye
        }),
        label=_("Lütfen bu alanı boş bırakın")  # Çeviri eklendi
    )

    # RECAPTCHA ALANI (Bot kalkanı)
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        label='', # Ekranda ekstra "Captcha:" yazmasına gerek yok
        error_messages={'required': _('Lütfen robot olmadığınızı doğrulayın.')} # Çeviri eklendi
    )

    class Meta:
        model = ContactMessage
        # fields listesine 'captcha'yı MUTLAKA ekliyoruz
        fields = ['name', 'email', 'subject', 'phone', 'message', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'yourName',
                'placeholder': _('Adınızı giriniz'),  # Çeviri eklendi
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'yourEmail',
                'placeholder': _('E-posta adresinizi giriniz'),  # Çeviri eklendi
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'yourSubject',
                'placeholder': _('Konu giriniz')  # Çeviri eklendi
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contactNumber',
                'placeholder': _('Telefon numaranızı giriniz')  # Çeviri eklendi
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message',
                'rows': 5,
                'placeholder': _('Bize birkaç kelime yazın'),  # Çeviri eklendi
                'required': True
            }),
        }

    # FORMU DOĞRULAMA (VALIDATION) ADIMI
    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('website_url')

        # Eğer honeypot alanı doluysa, bu bir bottur!
        if honeypot:
            # Hata mesajına da çeviri ekledik
            raise ValidationError(_("Form gönderiminde şüpheli bir işlem tespit edildi."))

        return cleaned_data
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))


from .models import GalleryItem
import re
from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = [
            "content_type", "image", "youtube_url",
            "title_tr", "title_en", "title_ar", "title_ru", "title_fr", "title_de"
        ]
        widgets = {
            "content_type": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "youtube_url": forms.URLInput(attrs={"class": "form-control"}),
            "title_tr": forms.TextInput(attrs={"class": "form-control"}),
            "title_en": forms.TextInput(attrs={"class": "form-control"}),
            "title_ar": forms.TextInput(attrs={"class": "form-control"}),
            "title_ru": forms.TextInput(attrs={"class": "form-control"}),
            "title_fr": forms.TextInput(attrs={"class": "form-control"}),
            "title_de": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.content_type == "video" and instance.youtube_url:
            video_id = None
            match = re.search(r"v=([a-zA-Z0-9_-]{11})", instance.youtube_url)
            if match:
                video_id = match.group(1)
            else:
                # youtu.be kısa link formatı
                match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", instance.youtube_url)
                if match:
                    video_id = match.group(1)

            if video_id:
                instance.youtube_thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        if commit:
            instance.save()
        return instance