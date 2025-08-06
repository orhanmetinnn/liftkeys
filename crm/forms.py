from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
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

class JobInfoForm(forms.ModelForm):
    class Meta:
        model = JobInfo
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Pozisyon / Ünvan'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Departman'
            }),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Aylık maaş (₺)'
            }),
            'work_location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Çalışma Lokasyonu (örn. İstanbul, Uzaktan)'
            }),
        }
