from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django import forms

# Kullanıcı ekleme ekranı için en basit form
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Şifreyi hash'ler
        if commit:
            user.save()
        return user

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Bu satır çok önemli: Ekleme ekranında yukarıdaki formu kullanmasını söyler
    add_form = CustomUserCreationForm 
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

    readonly_fields = ('last_login', 'date_joined') 

    # Düzenleme ekranı ayarları
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('İzinler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Önemli Tarihler', {'fields': ('last_login', 'date_joined')}),
    )

    # Yeni ekleme ekranı ayarları (confirm_password kaldırıldı)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password'), 
        }),
    )

# admin.site.register(CustomUser, CustomUserAdmin) -> @admin.register kullandığımız için buna gerek yok