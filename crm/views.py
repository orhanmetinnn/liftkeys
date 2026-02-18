from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.urls import reverse
from .models import Employee , JobInfo , TitlePersonel, Department, WorkLocation , Company,DirectoryCompany
from django.http import JsonResponse
from .forms import EmployeeForm , JobInfoForm ,TitlePersonelForm, DepartmentForm, WorkLocationForm,EmployeeUpdateForm , CompanyForm, SectorForm, CountryForm,UpdateCountryForm
from .forms import UpdateSectorForm,DirectoryCompanyForm
from django.db.models import Count 
import logging
from django.http import HttpResponseServerError
from .models import Employee , Sector,Country,Product,Category,Product,Opportunity
from .forms import EmployeeForm, EmployeeUpdateForm,UpdateCompanyForm,ProductForm,CategoryForm,OpportunityForm,UpdateOpportunityForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# logger = logging.getLogger('django')
"""
Personel Alanı
"""



# Logger oluştur
import logging

import logging
logger = logging.getLogger(__name__)
from functools import wraps


def employee_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'employee':
            return view_func(request, *args, **kwargs)
        return redirect('indexpage')  # yönlendirilecek sayfa (örn. hata sayfası)
    return _wrapped_view




@employee_required
@login_required
def employee_manage_view(request):
    logger.info("Employee yönetim sayfası açıldı.")
    employee_list = None
    form_create = EmployeeForm(prefix='create')
    form_update = EmployeeUpdateForm(prefix='update')
    selected_employee = None

    try:
        employee_list = Employee.objects.all()
        logger.debug(f"{employee_list.count()} çalışan listelendi.")
    except Exception as e:
        logger.exception("Çalışan listesi alınırken hata oluştu.")
        messages.error(request, 'Çalışan listesi alınırken bir hata oluştu.')
        employee_list = []

    if request.method == 'POST':
        logger.debug(f"Gelen POST verisi: {request.POST}")

        if 'create_submit' in request.POST:
            logger.info("Yeni çalışan ekleme isteği alındı.")
            form_create = EmployeeForm(request.POST, request.FILES, prefix='create')
            if form_create.is_valid():
                try:
                    # commit=False ile Employee objesini al
                    employee = form_create.save(commit=False)
                    employee.user = request.user  # login olan kullanıcıyı ata
                    employee.save()

                    logger.info("Yeni çalışan başarıyla kaydedildi.")
                    messages.success(request, 'Çalışan başarıyla kaydedildi.')
                    return redirect('employee_create')
                except Exception as e:
                    logger.exception("Yeni çalışan kaydedilirken hata oluştu.")
                    messages.error(request, 'Çalışan kaydedilirken bir hata oluştu.')
            else:
                logger.warning(f"Yeni çalışan formu geçersiz. Hatalar: {form_create.errors}")
                messages.error(request, 'Yeni çalışan formunda hata var.')

        # UPDATE işlemi
        elif 'update_submit' in request.POST:
            employee_id = request.POST.get('update_employee_id')
            logger.debug(f"Güncelleme için gelen çalışan ID: {employee_id}")

            if employee_id:
                try:
                    selected_employee = Employee.objects.get(pk=employee_id)
                    form_update = EmployeeUpdateForm(
                        request.POST, 
                        request.FILES, 
                        instance=selected_employee, 
                        prefix='update'
                    )
                    if form_update.is_valid():
                        employee = form_update.save(commit=False)
                        employee.user = request.user   # login olan kullanıcıyı bağla
                        employee.save()

                        logger.info(f"Çalışan (ID: {employee_id}) bilgileri güncellendi.")
                        messages.success(request, 'Çalışan bilgileri başarıyla güncellendi.')
                        return redirect('employee_create')
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_update.errors}")
                        messages.error(request, 'Güncelleme formunda hata var.')
                except Employee.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen çalışan bulunamadı. ID: {employee_id}")
                    messages.error(request, 'Güncellenecek çalışan bulunamadı.')
                except Exception as e:
                    logger.exception(f"Çalışan (ID: {employee_id}) güncellenirken beklenmeyen bir hata oluştu.")
                    messages.error(request, 'Güncelleme sırasında bir hata oluştu.')
            else:
                logger.error("Güncelleme isteğinde çalışan ID bilgisi eksik.")
                messages.error(request, 'Çalışan ID bilgisi eksik.')

    context = {
        'employee_list': employee_list,
        'form_create': form_create,
        'form_update': form_update,
        'selected_employee': selected_employee,
    }
    logger.debug("Sayfa context verileri hazırlandı.")
    return render(request, 'crmemployee.html', context)


def employee_detail_api(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    data = {
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'tc_identity': employee.tc_identity,
        'birth_date': employee.birth_date.strftime('%Y-%m-%d') if employee.birth_date else '',
        'gender': employee.gender,
        'email': employee.email,
        'phone_number': employee.phone,
        'address': employee.address,
        'start_date': employee.start_date.strftime('%Y-%m-%d') if employee.start_date else '',
        'is_active': employee.is_active,
    }
    return JsonResponse(data)



@employee_required
@login_required
def jobinfo_view(request):
    # Form nesneleri başta boş oluşturuluyor
    formjobinfo = JobInfoForm()
    formtitle = TitlePersonelForm()
    formdepartment = DepartmentForm()
    formworklocation = WorkLocationForm()

    if request.method == 'POST':
        # JobInfo create/update
        if 'submit_jobinfo' in request.POST:
            formjobinfo = JobInfoForm(request.POST)
            if formjobinfo.is_valid():
                employee = formjobinfo.cleaned_data.get('employee')

                # Zorunlu alanları al
                title = formjobinfo.cleaned_data.get('title')
                department = formjobinfo.cleaned_data.get('department')
                manager = formjobinfo.cleaned_data.get('manager')
                employment_type = formjobinfo.cleaned_data.get('employment_type')
                work_location = formjobinfo.cleaned_data.get('work_location')

                try:
                    jobinfo = JobInfo.objects.get(employee=employee)
                    # Eğer varsa güncelle
                    jobinfo.title = title
                    jobinfo.department = department
                    jobinfo.manager = manager
                    jobinfo.employment_type = employment_type
                    jobinfo.work_location = work_location
                    jobinfo.user = request.user
                    jobinfo.save()
                    messages.success(request, 'Çalışan bilgisi başarıyla güncellendi.')
                except JobInfo.DoesNotExist:
                    # Yoksa create
                    JobInfo.objects.create(
                        employee=employee,
                        title=title,
                        department=department,
                        manager=manager,
                        employment_type=employment_type,
                        work_location=work_location,
                        user=request.user
                    )
                    messages.success(request, 'Yeni çalışan bilgisi başarıyla eklendi.')

                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'İş bilgisi formunda hata var.')

        # TitlePersonel create
        elif 'submit_title' in request.POST:
            formtitle = TitlePersonelForm(request.POST)
            if formtitle.is_valid():
                title = formtitle.save(commit=False)
                title.user = request.user
                title.save()
                messages.success(request, 'Unvan başarıyla eklendi.')
                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'Unvan formunda hata var.')

        # Department create
        elif 'submit_department' in request.POST:
            formdepartment = DepartmentForm(request.POST)
            if formdepartment.is_valid():
                department = formdepartment.save(commit=False)
                department.user = request.user
                department.save()
                messages.success(request, 'Departman başarıyla eklendi.')
                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'Departman formunda hata var.')

        # WorkLocation create
        elif 'submit_worklocation' in request.POST:
            formworklocation = WorkLocationForm(request.POST)
            if formworklocation.is_valid():
                worklocation = formworklocation.save(commit=False)
                worklocation.user = request.user
                worklocation.save()
                messages.success(request, 'Çalışma lokasyonu başarıyla eklendi.')
                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'Çalışma lokasyonu formunda hata var.')

    context = {
        'formjobinfo': formjobinfo,
        'formtitle': formtitle,
        'formdepartment': formdepartment,
        'formworklocation': formworklocation
    }
    return render(request, 'crmjobinfo.html', context)


from django.db.models import Count, Prefetch
from django.utils.timezone import now
from django.db.models.functions import ExtractYear

@employee_required
@login_required
def report_employee(request):
    # JobInfo queryset, tüm ilişkilerle birlikte
    jobinfo_qs = JobInfo.objects.select_related('title', 'department', 'work_location', 'manager')

    # Employee queryset, JobInfo'yu prefetch ediyoruz
    employees = Employee.objects.prefetch_related(
        Prefetch('job_infos', queryset=jobinfo_qs)  # artık related_name 'job_infos'
    ).all()

    total_employees = employees.count()

    # Departman bazlı dağılım
    dept_distribution = JobInfo.objects.values('department__name').annotate(count=Count('id')).order_by('-count')

    # Cinsiyet dağılımı
    gender_distribution = employees.values('gender').annotate(count=Count('id'))

    # Çalışma tipi dağılımı
    employment_type_distribution = JobInfo.objects.values('employment_type').annotate(count=Count('id'))

    # Yıllara göre işe başlama sayısı (son 5 yıl örneği)
    current_year = now().year
    employment_years = Employee.objects.annotate(year=ExtractYear('start_date')) \
        .values('year') \
        .annotate(count=Count('id')) \
        .filter(year__gte=current_year - 5) \
        .order_by('year')

    context = {
        'employees': employees,
        'total_employees': total_employees,
        'dept_distribution': list(dept_distribution),
        'gender_distribution': list(gender_distribution),
        'employment_type_distribution': list(employment_type_distribution),
        'employment_years': list(employment_years),
    }

    return render(request, 'reportemployee.html', context)



"""
Firma Alanı
"""




@employee_required
@login_required
def company_manage_view(request):

    company_list = None
    form_create = CompanyForm(prefix='create')
    form_update = CompanyForm(prefix='update')
    selected_company = None
    ulke_list = None
    sector_list = None

    try:
        company_list = Company.objects.all()
        logger.debug(f"{company_list.count()} firma listelendi.")
    except Exception as e:
        logger.exception("Firma listesi alınırken hata oluştu.")
        messages.error(request, 'Firma listesi alınırken bir hata oluştu.')
        company_list = []

    try:
        ulke_list = Country.objects.all()
        logger.debug(f"{ulke_list.count()} ulke listelendi.")
    except Exception as e:
        logger.exception("Ulke listesi alınırken hata oluştu.")
        messages.error(request, 'Ulke listesi alınırken bir hata oluştu.')
        ulke_list = []

    try:
        sector_list = Sector.objects.all()
        logger.debug(f"{sector_list.count()} sektor listelendi.")
    except Exception as e:
        logger.exception("Sektor listesi alınırken hata oluştu.")
        messages.error(request, 'Sektor listesi alınırken bir hata oluştu.')
        sector_list = []

    if request.method == 'POST':
        logger.debug(f"Gelen POST verisi: {request.POST}")

        # CREATE COMPANY
        if 'create_submit' in request.POST:
            logger.info("Yeni firma ekleme isteği alındı.")
            form_create = CompanyForm(request.POST, prefix='create')
            if form_create.is_valid():
                try:
                    company_obj = form_create.save(commit=False)
                    company_obj.user = request.user  # 🔑 GİRİŞ YAPAN KULLANICI
                    company_obj.save()
                    logger.info("Yeni firma başarıyla kaydedildi.")
                    messages.success(request, 'Firma başarıyla kaydedildi.')
                    return redirect('company_manage')
                except Exception as e:
                    logger.exception("Yeni firma kaydedilirken hata oluştu.")
                    messages.error(request, 'Firma kaydedilirken bir hata oluştu.')
            else:
                logger.warning(f"Yeni firma formu geçersiz. Hatalar: {form_create.errors}")
                messages.error(request, 'Yeni firma formunda hata var.')

        # UPDATE COMPANY
        elif 'update_submit' in request.POST:
            company_id = request.POST.get('update_company_id')
            logger.debug(f"Güncelleme için gelen firma ID: {company_id}")

            if company_id:
                try:
                    selected_company = Company.objects.get(pk=company_id)
                    form_update = UpdateCompanyForm(request.POST, instance=selected_company, prefix='update')
                    if form_update.is_valid():
                        company_obj = form_update.save(commit=False)
                        company_obj.user = request.user  # 🔑 Güncelleyen kullanıcıyı kaydet
                        company_obj.save()
                        logger.info(f"Firma (ID: {company_id}) bilgileri güncellendi.")
                        messages.success(request, 'Firma bilgileri başarıyla güncellendi.')
                        return redirect('company_manage')
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_update.errors}")
                        messages.error(request, 'Güncelleme formunda hata var.')
                except Company.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen firma bulunamadı. ID: {company_id}")
                    messages.error(request, 'Güncellenecek firma bulunamadı.')
                except Exception as e:
                    logger.exception(f"Firma (ID: {company_id}) güncellenirken hata oluştu.")
                    messages.error(request, 'Güncelleme sırasında bir hata oluştu.')
            else:
                logger.error("Güncelleme isteğinde firma ID bilgisi eksik.")
                messages.error(request, 'Firma ID bilgisi eksik.')

        # CREATE COUNTRY
        elif 'create_country_submit' in request.POST:
            logger.info("Yeni ülke ekleme isteği alındı.")
            form_country = CountryForm(request.POST, prefix='country')
            if form_country.is_valid():
                try:
                    country_obj = form_country.save(commit=False)
                    country_obj.user = request.user  # 🔑 giriş yapan kullanıcıyı kaydet
                    country_obj.save()
                    logger.info("Yeni ülke başarıyla kaydedildi.")
                    messages.success(request, 'Ülke başarıyla kaydedildi.')
                    return redirect('company_manage')
                except Exception as e:
                    logger.exception("Yeni ülke kaydedilirken hata oluştu.")
                    messages.error(request, 'Ülke kaydedilirken hata oluştu.')
            else:
                logger.warning(f"Yeni ülke formu geçersiz. Hatalar: {form_country.errors}")
                messages.error(request, 'Ülke formunda hata var.')

        # UPDATE COUNTRY
        elif 'update_country_submit' in request.POST:
            country_id = request.POST.get('update_country_id')
            logger.debug(f"Güncelleme için gelen ülke ID: {country_id}")
            if country_id:
                try:
                    selected_country = Country.objects.get(pk=country_id)
                    form_country = UpdateCountryForm(request.POST, instance=selected_country, prefix='update')
                    if form_country.is_valid():
                        country_obj = form_country.save(commit=False)
                        country_obj.user = request.user
                        country_obj.save()
                        logger.info(f"Ülke (ID: {country_id}) başarıyla güncellendi.")
                        messages.success(request, 'Ülke başarıyla güncellendi.')
                        return redirect('company_manage')
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_country.errors}")
                        messages.error(request, 'Ülke güncelleme formunda hata var.')
                except Country.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen ülke bulunamadı. ID: {country_id}")
                    messages.error(request, 'Güncellenecek ülke bulunamadı.')
                except Exception as e:
                    logger.exception(f"Ülke (ID: {country_id}) güncellenirken hata oluştu.")
                    messages.error(request, 'Ülke güncelleme sırasında hata oluştu.')
            else:
                logger.error("Ülke güncelleme isteğinde ID eksik.")
                messages.error(request, 'Ülke ID bilgisi eksik.')

        # CREATE SECTOR
        elif 'create_sector_submit' in request.POST:
            logger.info("Yeni sektör ekleme isteği alındı.")
            form_sector = SectorForm(request.POST, prefix='sector')
            if form_sector.is_valid():
                try:
                    sector_obj = form_sector.save(commit=False)
                    sector_obj.user = request.user
                    sector_obj.save()
                    logger.info("Yeni sektör başarıyla kaydedildi.")
                    messages.success(request, 'Sektör başarıyla kaydedildi.')
                    return redirect('company_manage')
                except Exception as e:
                    logger.exception("Yeni sektör kaydedilirken hata oluştu.")
                    messages.error(request, 'Sektör kaydedilirken hata oluştu.')
            else:
                logger.warning(f"Yeni sektör formu geçersiz. Hatalar: {form_sector.errors}")
                messages.error(request, 'Sektör formunda hata var.')

        # UPDATE SECTOR
        elif 'update_sector_submit' in request.POST:
            sector_id = request.POST.get('update_sector_id')
            logger.debug(f"Güncelleme için gelen sektör ID: {sector_id}")
            if sector_id:
                try:
                    selected_sector = Sector.objects.get(pk=sector_id)
                    form_sector = UpdateSectorForm(request.POST, instance=selected_sector, prefix='update')
                    if form_sector.is_valid():
                        sector_obj = form_sector.save(commit=False)
                        sector_obj.user = request.user
                        sector_obj.save()
                        logger.info(f"Sektör (ID: {sector_id}) başarıyla güncellendi.")
                        messages.success(request, 'Sektör başarıyla güncellendi.')
                        return redirect('company_manage')
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_sector.errors}")
                        messages.error(request, 'Sektör güncelleme formunda hata var.')
                except Sector.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen sektör bulunamadı. ID: {sector_id}")
                    messages.error(request, 'Güncellenecek sektör bulunamadı.')
                except Exception as e:
                    logger.exception(f"Sektör (ID: {sector_id}) güncellenirken hata oluştu.")
                    messages.error(request, 'Sektör güncelleme sırasında hata oluştu.')
            else:
                logger.error("Sektör güncelleme isteğinde ID eksik.")
                messages.error(request, 'Sektör ID bilgisi eksik.')

    context = {
        'company_list': company_list,
        'form_create': CompanyForm(prefix='create'),
        'form_update': UpdateCompanyForm(prefix='update'),
        'selected_company': selected_company,
        'form_create_country': CountryForm(prefix='country'),
        'form_update_country': UpdateCountryForm(prefix='update'),
        'selected_country': locals().get('selected_country'),
        'form_create_sector': SectorForm(prefix='sector'),
        'form_update_sector': UpdateSectorForm(prefix='update'),
        'selected_sector': locals().get('selected_sector'),
        'country_list': ulke_list,
        'sector_list': sector_list,
    }
    logger.debug("Sayfa context verileri hazırlandı.")
    return render(request, 'firmayonetim/companycreatandupdate.html', context)



def company_detail_api(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    
    data = {
        'id': company.id,
        'firma_adi': company.firma_adi,
        'vergi_no': company.vergi_no,
        'sektor': company.sektor.name if company.sektor else None,
        'telefon': company.telefon,
        'telefon2': company.telefon2,
        'fax': company.fax,
        'email': company.email,
        'email2': company.email2,
        'websitesi': company.websitesi,
        'adres': company.adres,
        'sehir': company.sehir,
        'ilce': company.ilce,
        'posta_kodu': company.posta_kodu,
        'ulke': company.ulke.name if company.ulke else None,
        'kurulus_tarihi': company.kurulus_tarihi.strftime('%Y-%m-%d') if company.kurulus_tarihi else '',
        'calisan_sayisi': company.calisan_sayisi,
        'netciiro': str(company.netciiro) if company.netciiro is not None else None,
        'sektor_alt_bilgisi': company.sektor_alt_bilgisi,
        'yetkili_adi': company.yetkili_adi,
        'yetkili_pozisyon': company.yetkili_pozisyon,
        'yetkili_telefon': company.yetkili_telefon,
        'yetkili_email': company.yetkili_email,
        'linkedin': company.linkedin,
        'twitter': company.twitter,
        'facebook': company.facebook,
        'instagram': company.instagram,
        'aktif_mi': company.aktif_mi,
        'notlar': company.notlar,
    }
    
    return JsonResponse(data)






def sector_detail_api(request, sector_id):
    sector = get_object_or_404(Sector, pk=sector_id)

    data = {
        'id': sector.id,
        'name': sector.name,
        # Eğer user alanını da göstermek istersen:
        # 'user': sector.user.username if sector.user else None,
    }

    return JsonResponse(data)


def country_detail_api(request, country_id):
    country = get_object_or_404(Country, pk=country_id)

    data = {
        'id': country.id,
        'name': country.name,
        'code': country.code,
        # Eğer user alanını da göstermek istersen:
        # 'user': country.user.username if country.user else None,
    }

    return JsonResponse(data)



@employee_required
@login_required
def directory_company_update(request):
    try:
        if request.method == 'POST':
            form = DirectoryCompanyForm(request.POST)
            if form.is_valid():
                # Kullanıcıyı eklemek için commit=False
                directory_obj = form.save(commit=False)
                directory_obj.user = request.user  # 🔑 Giriş yapan kullanıcı kaydediliyor
                directory_obj.save()

                messages.success(request, "Bilgiler başarıyla kaydedildi.")
                logger.info(f"DirectoryCompany yeni kaydı oluşturuldu. Kullanıcı: {request.user}")
                return redirect('directory_company_update')
            else:
                messages.error(request, "Formda hatalar var, lütfen kontrol edin.")
                logger.warning(f"DirectoryCompany form doğrulama hatası: {form.errors}")
        else:
            form = DirectoryCompanyForm()

        all_companies_list = DirectoryCompany.objects.all().order_by('-created_at')

        # Sayfalama
        page = request.GET.get('page', 1)
        paginator = Paginator(all_companies_list, 10)

        try:
            all_companies = paginator.page(page)
        except PageNotAnInteger:
            all_companies = paginator.page(1)
        except EmptyPage:
            all_companies = paginator.page(paginator.num_pages)

        context = {
            'formrehberekle': form,
            'all_companies': all_companies,
        }
        return render(request, 'firmayonetim/companydirectory.html', context)

    except Exception as e:
        logger.error(f"DirectoryCompany view'da hata: {e}", exc_info=True)
        return HttpResponseServerError("Bir hata oluştu, lütfen daha sonra tekrar deneyin.")






"""
URUNLER
"""

from .forms import ProductForm, CategoryForm, ProductMarketImageFormSet
from .models import Category, Product, ProductMarketImage

from .models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .forms import (
    CategoryForm,
    ProductForm,
    ProductMarketImageFormSet,
)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Product
from .forms import ProductForm, ProductMarketImageFormSet
from .forms import ProductForm, ProductMarketImageFormSet, ProductQuestionFormSet

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction

from .models import Product,ProductQuestion,ProductQuestionOption
from .forms import ProductForm, ProductMarketImageFormSet, ProductQuestionFormSet,ProductQuestionOptionFormSet


@employee_required
@login_required
def product_hub(request):
    # Ürünleri listele
    products = Product.objects.prefetch_related("categories", "market_images").order_by("-created_at")
    current_id = request.GET.get("id")
    instance = Product.objects.filter(pk=current_id).first() if current_id else None

    if request.method == "GET":
        product_form = ProductForm(prefix="product", instance=instance)
        images_formset = ProductMarketImageFormSet(prefix="images", instance=(instance or Product()))

        return render(request, "urunler/uruncreateandupdate.html", {
            "products": products,
            "product_form": product_form,
            "images_formset": images_formset,
            "editing": bool(instance),
            "current_id": current_id or "",
        })

    # POST işlemi
    action = request.POST.get("action", "create")
    if action not in ("create", "update"):
        messages.error(request, "Geçersiz işlem.")
        return redirect(reverse("product_hub"))

    if action == "update":
        current_id = request.POST.get("product_id")
        instance = get_object_or_404(Product, pk=current_id)

    product_form = ProductForm(request.POST, request.FILES, prefix="product", instance=instance)

    try:
        with transaction.atomic():
            # Formset'i burada tanımlamak daha sağlıklı, instance'ı birazdan vereceğiz ama
            # validation için POST verisiyle başlatmamız lazım.
            # Ancak instance henüz save edilmediği için formset validasyonunda dikkatli olmalıyız.
            # Kod akışını bozmamak için senin yapını koruyarak ilerliyorum.
            
            if not product_form.is_valid():
                messages.error(request, "Lütfen ürün formundaki hataları düzeltin.")
                return render(request, "urunler/uruncreateandupdate.html", {
                    "products": products,
                    "product_form": product_form,
                    "images_formset": ProductMarketImageFormSet(request.POST, request.FILES, prefix="images", instance=(instance or Product())),
                    "editing": action == "update",
                    "current_id": current_id or "",
                })

            # 1. Ürün nesnesi oluştur ama hemen kaydetme (commit=False)
            product = product_form.save(commit=False)
            product.user = request.user  # 🔑 Giriş yapan kullanıcıyı kaydet
            
            # 2. Ana ürünü kaydet (Artık bir ID'si var)
            product.save()

            # 🔥🔥🔥 KRİTİK DÜZELTME BURASI 🔥🔥🔥
            # commit=False kullandığımız için ManyToMany (Kategoriler) elle kaydedilmeli:
            product_form.save_m2m() 
            # -------------------------------------

            # 3. Görselleri kaydet
            images_formset = ProductMarketImageFormSet(request.POST, request.FILES, prefix="images", instance=product)
            
            if images_formset.is_valid():
                images = images_formset.save(commit=False)
                
                # Silinen görselleri işle (commit=False olduğu için bunu da elle yapmalısın)
                for deleted_object in images_formset.deleted_objects:
                    deleted_object.delete()
                
                # Yeni veya güncellenen görselleri kaydet
                for img in images:
                    img.user = request.user  # 🔑 Görseli ekleyen kullanıcı
                    img.save()
                
                messages.success(request, f"‘{product.name}’ başarıyla kaydedildi.")
                return redirect(f"{reverse('product_hub')}?id={product.id}")
            else:
                # print("Image Formset Errors:", images_formset.errors)
                messages.error(request, "Lütfen görsel formundaki hataları düzeltin.")
                return render(request, "urunler/uruncreateandupdate.html", {
                    "products": products,
                    "product_form": product_form,
                    "images_formset": images_formset,
                    "editing": action == "update",
                    "current_id": product.id,
                })

    except Exception as e:
        # Hata detayını görmek için print ekleyebilirsin
        # print(f"HATA DETAYI: {e}") 
        messages.error(request, f"Hata oluştu: {e}")
        return redirect(reverse("product_hub"))



from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
@employee_required
@login_required
def product_questions_view(request, product_id):
    """
    Belirli bir ürünün sorularını ve şıklarını yönetir.
    """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        question_formset = ProductQuestionFormSet(request.POST, instance=product, prefix="questions")

        option_formsets = []
        option_formsets_valid = True

        if question_formset.is_valid():
            with transaction.atomic():
                # Soruları kaydetmeden önce user ekle
                questions = question_formset.save(commit=False)
                for q in questions:
                    q.user = request.user
                    q.save()

                # Silinecek sorular varsa sil
                for q in question_formset.deleted_objects:
                    q.delete()

                # Option formsetlerini doğrula
                for q_form in question_formset.forms:
                    q_instance = q_form.instance
                    opt_prefix = f"options-{q_form.prefix}"
                    opt_formset = ProductQuestionOptionFormSet(
                        request.POST, instance=q_instance, prefix=opt_prefix
                    )
                    option_formsets.append(opt_formset)
                    if not opt_formset.is_valid():
                        option_formsets_valid = False

                if option_formsets_valid:
                    for opt_formset in option_formsets:
                        option_instances = opt_formset.save(commit=False)
                        for opt in option_instances:
                            opt.user = request.user
                            opt.save()
                        for deleted_opt in opt_formset.deleted_objects:
                            deleted_opt.delete()

                    messages.success(request, "Sorular ve şıklar başarıyla kaydedildi.")
                    return redirect(reverse("product_questions", kwargs={"product_id": product.id}))
                else:
                    messages.error(request, "Lütfen şık alanlarındaki hataları düzeltin.")
        else:
            messages.error(request, "Lütfen soru alanlarındaki hataları düzeltin.")
    else:
        question_formset = ProductQuestionFormSet(instance=product, prefix="questions")
        option_formsets = []
        for q_form in question_formset.forms:
            opt_prefix = f"options-{q_form.prefix}"
            opt_formset = ProductQuestionOptionFormSet(instance=q_form.instance, prefix=opt_prefix)
            option_formsets.append(opt_formset)

    q_groups = []
    for idx, q_form in enumerate(question_formset.forms):
        q_groups.append({
            "q_form": q_form,
            "opt_formset": option_formsets[idx] if idx < len(option_formsets) else ProductQuestionOptionFormSet(
                instance=q_form.instance, prefix=f"options-{q_form.prefix}"
            ),
        })

    return render(request, "productmanager/product_questions.html", {
        "product": product,
        "question_formset": question_formset,
        "q_groups": q_groups,
    })





from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductQuestion, ProductAnswer
from .utils import add_to_cart

def add_to_cart_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # <-- JSON'u parse et
            product_id = data.get("product_id")
            qty = int(data.get("qty", 1))
            answers = data.get("answers", {})

            product = get_object_or_404(Product, id=product_id)

            # Soruları kaydet
            for q_id, value in answers.items():
                q = product.questions.filter(id=q_id).first()
                if q:
                    ProductAnswer.objects.create(
                        product=product,
                        question=q,
                        user=request.user if request.user.is_authenticated else None,
                        session_key=request.session.session_key,
                        answer_text=", ".join(value) if isinstance(value, list) else value
                    )

            add_to_cart(request, product.id, answers, qty=qty)

            return JsonResponse({"message": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)




def cart_summary_api(request):
    # print("CART_SUMMARY -> Session Key:", request.session.session_key)
    # print("burasi çalıştı")
    cart = request.session.get("cart", [])
    product_ids = [item["product_id"] for item in cart]
    products = Product.objects.in_bulk(product_ids)

    items = []
    total_count = 0

    for item in cart:
        pid = item.get("product_id")
        qty = item.get("qty", 1)
        product = products.get(pid)
        
        if not product:
            continue

        items.append({
            "id": product.id,
            "name": product.name,
            "price": f"{product.price} {product.currency or ''}".strip(),
            "image": product.website_image.url if product.website_image else "",
            "qty": qty,
            "answers": item.get("answers", {}),
        })
        total_count += qty

    # print("CART_SUMMARY -> Session Key:", request.session.session_key)
    # print("CART_SUMMARY -> Cart:", cart)

    return JsonResponse({"items": items, "total_count": total_count})

def cart_page(request):
    cart = request.session.get("cart", [])
    products = []
    for item in cart:
        try:
            product = Product.objects.get(id=item["product_id"])
            products.append({
                "product": product,
                "answers": item.get("answers", {}),
                "qty": item.get("qty", 1)
            })
        except Product.DoesNotExist:
            continue

    return render(request, "productmanager/card_page.html", {"cart_items": products})


import json
def add_to_cart(request):
    if not request.session.session_key:
        request.session.create()

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Geçersiz veri"}, status=400)

    # 🔑 product_id'yi integera çevir
    try:
        product_id = int(data.get("product_id"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Geçersiz product_id"}, status=400)

    qty = int(data.get("qty", 1))
    answers = data.get("answers", {})

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", [])

    found = False
    for item in cart:
        if item["product_id"] == product_id and item.get("answers") == answers:
            item["qty"] = item.get("qty", 1) + qty
            found = True
            break

    if not found:
        cart.append({"product_id": product_id, "answers": answers, "qty": qty})

    request.session["cart"] = cart
    request.session.modified = True
    request.session.save()

    # print("🛒 Cart after add:", request.session["cart"], "Session Key:", request.session.session_key)

    total_count = sum(item.get("qty", 1) for item in cart)
    return JsonResponse({"success": True, "cart_count": total_count})




def update_cart(request):
    """Sepetteki ürünleri güncellemek için kullanılır (AJAX)."""
    if request.method == "POST":
        data = json.loads(request.body)
        index = data.get("index")
        action = data.get("action")  # "increase", "decrease", "remove"
        cart = request.session.get("cart", [])

        if 0 <= index < len(cart):
            if action == "remove":
                cart.pop(index)
            elif action == "increase":
                cart.append(cart[index])  # aynı ürünü bir tane daha ekle
            elif action == "decrease" and cart.count(cart[index]) > 1:
                cart.remove(cart[index])

            request.session["cart"] = cart
            request.session.modified = True
            return JsonResponse({"success": True, "cart_count": len(cart)})

    return JsonResponse({"success": False})


from .models import Order, OrderItem

def cart_checkout(request):
    cart = request.session.get("cart", [])

    # 🟢 Product nesnelerini alalım
    cart_items = []
    for item in cart:
        product = Product.objects.filter(id=item["product_id"]).first()
        if product:
            cart_items.append({
                "product": product,
                "qty": item.get("qty", 1),
                "answers": item.get("answers", {})
            })

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message_text = request.POST.get("message")

        # 1️⃣ Order oluştur
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            phone=phone,
            message=message_text,
            session_key=request.session.session_key
        )

        # 2️⃣ OrderItem kaydet
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                qty=item["qty"],
                answers=item["answers"]
            )

        # 3️⃣ Sepeti temizle
        request.session["cart"] = []
        request.session.modified = True

        messages.success(request, f"Siparişiniz başarıyla alındı! Sipariş Numaranız: #{order.id}")
        return redirect("cart_page")

    return render(request, "productmanager/checkout.html", {"cart_items": cart_items})







def catogory_detail_api(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    data = {
        'id': category.id,
        'name': category.name,
    }
    return JsonResponse(data)




from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .models import ProductPage

def category_list(request):
    # Sadece menüde gösterilsin işaretli kategoriler
    categories = Category.objects.filter(menude_goster=True, parent__isnull=True)
    return render(request, "productmanager/category_list.html", {"categories": categories})


def category_detail(request, slug):
    # Seçili kategori
    category = get_object_or_404(Category, slug=slug)

    # Bu kategoriye bağlı ürünler
    products = Product.objects.filter(categories=category, is_active=True)

    # Ana kategoriler (sidebar'ın üst kısmı için)
    categories = Category.objects.filter(menude_goster=True, parent__isnull=True)

    # ALT kategoriler (sidebar'da göstermek için)
    subcategories = Category.objects.filter(parent=category)

    return render(request, "productmanager/category_detail.html", {
        "category": category,
        "products": products,
        "categories": categories,
        "subcategories": subcategories,      # ✅ ekledik
        "selected_category": category
    })




@employee_required
@login_required
def OpportunityDetail(request):
    try:
        Opportunity_list = Opportunity.objects.all()
        logger.debug(f"{Opportunity_list.count()} fırsat listelendi.")
    except Exception as e:
        logger.exception("Fırsat listesi alınırken hata oluştu.")
        messages.error(request, 'Fırsat listesi alınırken bir hata oluştu.')
        Opportunity_list = []

    if request.method == 'POST':
        form_create = OpportunityForm(request.POST, prefix='create')

        # CREATE
        if 'create_opportunity_submit' in request.POST:
            if form_create.is_valid():
                opportunity = form_create.save(commit=False)
                opportunity.user = request.user  # 🔑 Login olan kullanıcıyı kaydet
                opportunity.save()
                form_create.save_m2m()  # M2M alanları (products) kaydedilmeli
                logger.info("Yeni fırsat başarıyla kaydedildi.")
                messages.success(request, 'Fırsat başarıyla kaydedildi.')
                return redirect('OpportunityDetail')
            else:
                logger.warning(f"Yeni fırsat formu geçersiz. Hatalar: {form_create.errors}")
                messages.error(request, 'Yeni fırsat formunda hata var.')

        # UPDATE
        elif 'update_opportunity_submit' in request.POST:
            opportunity_id = request.POST.get('update-id')
            logger.debug(f"Güncelleme için gelen fırsat ID: {opportunity_id}")
            
            if opportunity_id:
                try:
                    selected_opportunity = get_object_or_404(Opportunity, pk=opportunity_id)
                    form_update = UpdateOpportunityForm(request.POST, instance=selected_opportunity, prefix='update')

                    if form_update.is_valid():
                        opportunity = form_update.save(commit=False)
                        opportunity.user = request.user  # 🔑 Güncelleyen kullanıcı kaydedilir
                        opportunity.save()
                        form_update.save_m2m()
                        logger.info(f"Fırsat (ID: {opportunity_id}) başarıyla güncellendi.")
                        messages.success(request, 'Fırsat başarıyla güncellendi.')
                        return redirect('OpportunityDetail')
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_update.errors}")
                        messages.error(request, 'Fırsat güncelleme formunda hata var.')
                except Opportunity.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen fırsat bulunamadı. ID: {opportunity_id}")
                    messages.error(request, 'Güncellenecek fırsat bulunamadı.')
                except Exception as e:
                    logger.exception(f"Fırsat (ID: {opportunity_id}) güncellenirken hata oluştu: {e}")
                    messages.error(request, 'Fırsat güncelleme sırasında hata oluştu.')
            else:
                logger.error("Fırsat güncelleme isteğinde ID eksik.")
                messages.error(request, 'Fırsat ID bilgisi eksik.')

    context = {
        'formOpportunityCreate': OpportunityForm(prefix='create'),
        'formOpportunityUpdate': UpdateOpportunityForm(prefix='update'),
        'Opportunity_list': Opportunity_list,
    }
    return render(request, 'fırsatlar/opportunity.html', context)






def opportunity_detail_api(request, opportunity_id):
    try:
        opportunity = Opportunity.objects.get(pk=opportunity_id)
        data = {
            'id': opportunity.id,
            'name': opportunity.name,
            'company': {
                'id': opportunity.company.id,
                'firma_adi': opportunity.company.firma_adi
            },
            'products': list(opportunity.products.values(
                'id', 'name', 'stock_code', 'price'
            )),
            'description': opportunity.description,
            'status': opportunity.status,
            'priority': opportunity.priority,
            'estimated_value': str(opportunity.estimated_value) if opportunity.estimated_value else None,
            'expected_close_date': opportunity.expected_close_date.strftime('%Y-%m-%d') if opportunity.expected_close_date else None,
            'lead_source': opportunity.lead_source,
            'owner': {
                'id': opportunity.owner.id,
                'name': f"{opportunity.owner.first_name} {opportunity.owner.last_name}"
            } if opportunity.owner else None,
            'created_at': opportunity.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': opportunity.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse(data)

    except Opportunity.DoesNotExist:
        return JsonResponse({'error': 'Fırsat bulunamadı'}, status=404)












from .models import Offer, OfferProduct
from .forms import OfferForm, OfferProductFormSet




def get_products_by_category(request, category_id):
    products = Product.objects.filter(categories__id=category_id)
    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "currency": p.currency,
            "image": p.website_image.url if p.website_image else ""
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)






def offer_create(request):
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES)
        formset = OfferProductFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            try:
                offer = form.save()
                offer_products = formset.save(commit=False)
                for op in offer_products:
                    op.offer = offer
                    op.save()
                messages.success(request, "Teklif başarıyla oluşturuldu.")
                return redirect("offer_create")
            except Exception as e:
                # Hata detayını gör
                messages.error(request, f"Kaydederken hata oluştu: {str(e)}")
        else:
            # Form ve formset hatalarını göster
            # print("Form Hataları:", form.errors)
            # print("Formset Hataları:", formset.errors)
            messages.error(request, "Formda hata var. Lütfen kontrol edin.")
    else:
        form = OfferForm()
        formset = OfferProductFormSet()
    
    products = Product.objects.all()
    categories = Category.objects.all() 
    return render(request, "teklifler/offer_create.html", {
        "form": form,
        "formset": formset,
        "products": products,
        "categories": categories,
    })


# Teklif listesi
def offer_list(request):
    offers = Offer.objects.all().order_by('-created_at')
    return render(request, "teklifler/offer_list.html", {"offers": offers})


# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from .models import Offer, OfferProduct  # OfferProduct: formset ile ilişkilendirilen model

# from django.shortcuts import get_object_or_404
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from weasyprint import HTML

# from django.conf import settings
# import os

# def offer_pdf(request, offer_id):
#     offer = get_object_or_404(Offer, id=offer_id)
#     products = offer.offerproduct_set.all()

#     total_price = sum(op.final_price or 0 for op in products)

#     context = {
#         "offer": offer,
#         "products": products,
#         "total_price": total_price,
#     }

#     html_string = render_to_string("teklifler/offer_pdf.html", context)

#     # base_url ile medya ve static dosyalarını çöz
#     pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
#     response = HttpResponse(pdf_file, content_type="application/pdf")
#     response["Content-Disposition"] = f'inline; filename="offer_{offer_id}.pdf"'
#     return response



# from weasyprint import HTML, CSS
# from django.template.loader import render_to_string
# from django.http import HttpResponse

# def offer_pdf(request, offer_id):
#     offer = get_object_or_404(Offer, pk=offer_id)
#     html_string = render_to_string("teklifler/offer_pdf.html", {"offer": offer})
#     pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

#     response = HttpResponse(pdf_file, content_type="application/pdf")
#     response['Content-Disposition'] = f'inline; filename="offer_{offer_id}.pdf"'
#     return response




@employee_required
@login_required
def category_manage(request, pk=None):
    if pk:
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
        title = 'Kategori Güncelle'
    else:
        category = None
        form = CategoryForm(request.POST or None, request.FILES or None)
        title = 'Yeni Kategori Oluştur'

    if request.method == 'POST':
        if form.is_valid():
            category_obj = form.save(commit=False)
            category_obj.user = request.user  # giriş yapan kullanıcıyı kaydet

            # 🟢 Debug logları - terminalde görebilirsin
            # print("FORM CLEANED DATA:", form.cleaned_data)

            category_obj.save()
            form.save_m2m()

            messages.success(request, "Kategori başarıyla kaydedildi.")
            return redirect('category_manage')
        else:
            # Eğer form valid değilse hataları logla
            # print("FORM ERRORS:", form.errors)
            messages.error(request, "Kategori kaydedilirken hata oluştu.")

    categories = Category.objects.all()
    return render(request, 'urunler/category_form.html', {
        'form': form,
        'categories': categories,
        'title': title,
        'editing': category is not None
    })



"""Ana sayfa"""


from django.utils import translation
def indexpage(request):
    # print(">>> Aktif dil:", translation.get_language())
    # Menüde gösterilecek kategoriler
    menu_categories = Category.objects.filter(menude_goster=True).order_by('name')

    # Her kategoriye bağlı ürünleri attribute olarak ekle
    for cat in menu_categories:
        cat.products = Product.objects.filter(categories=cat, is_active=True)

    context = {
        'menu_categories': menu_categories,
    }
    return render(request, 'preview/index.html', context)


from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContactForm
def contactpage(request):
    # Menüde gösterilecek kategoriler
    menu_categories = Category.objects.filter(menude_goster=True).order_by('name')

    # Her kategoriye bağlı ürünleri attribute olarak ekle
    for cat in menu_categories:
        cat.products = Product.objects.filter(categories=cat, is_active=True)
    if request.method == "POST":
        # print("post geldi")
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Artık güvenli
            messages.success(request, "Mesajınız başarıyla gönderildi!")
            return redirect('contact')  # Aynı sayfa
                
    else:
        form = ContactForm()

    context = {
        'menu_categories': menu_categories,
        'form': form,
    }
    return render(request, 'preview/contactpage.html', context)




def contact_form_view_preview(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız."})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    return JsonResponse({"success": False, "message": "Geçersiz istek."}, status=405)



from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage

from django.core.paginator import Paginator

def crm_contact_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')

    paginator = Paginator(messages_list, 10)  # her sayfada 10 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'iletisimcrmpage/contact_messages.html', {
        'page_obj': page_obj
    })

from django.views.decorators.http import require_POST
@require_POST
def crm_toggle_contacted(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.contacted = not msg.contacted
    msg.save()
    return redirect('crm_contact_messages')




from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Category, Product

def loginorcreate(request):
    # Menüde gösterilecek kategoriler
    menu_categories = Category.objects.filter(menude_goster=True).order_by('name')
    for cat in menu_categories:
        cat.products = Product.objects.filter(categories=cat, is_active=True)

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            # Giriş formu gönderildi
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                
                # Role göre yönlendirme
                if user.role == 'employee':
                    return redirect('company_manage')
                else:  # customer veya diğer roller
                    return redirect('indexpage')
            else:
                messages.error(request, "E-posta veya şifre yanlış.")
        
        elif 'register_submit' in request.POST:
            # Kayıt formu gönderildi
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.role = 'customer'  # default rol
                user.save()
                login(request, user)
                return redirect('indexpage')
            else:
                messages.error(request, "Formda hata var, lütfen kontrol edin.")
    else:
        form = CustomUserCreationForm()

    context = {
        'menu_categories': menu_categories,
        'form': form
    }
    return render(request, 'preview/loginorcreate.html', context)


from .models import Order
@login_required
def order_list(request):
    orders = (
        Order.objects.select_related("user")
        .prefetch_related("items__product")
        .order_by("is_processed", "-created_at")  # Önce beklemede, sonra tarihe göre
    )
    return render(request, "order/crmorder.html", {"orders": orders})


@login_required
def toggle_order_status(request, pk):
    """AJAX ile işleme geçildi durumunu değiştirir"""
    if request.method == "POST":
        order = get_object_or_404(Order, pk=pk)
        order.is_processed = not order.is_processed
        order.save()
        return JsonResponse({
            "success": True,
            "new_status": order.is_processed
        })
    return JsonResponse({"success": False}, status=400)



from django.shortcuts import render

def about_view(request):
    """
    Liftkeys hakkımızda sayfasını render eder.
    """
    return render(request, "preview/about.html")










def privacy_view(request):
    """
    Gizlilik Politikası sayfasını render eder.
    """
    return render(request, "preview/gizlilikguvenlik.html")



def custom_404(request, exception=None):
    """
    Özel 404 sayfası view.
    """
    return render(request, "404.html", status=404)




from .models import GalleryItem
def gallery_view(request):
    return render(request, "preview\gallery.html")

def gallery_items_api(request):
    offset = int(request.GET.get("offset", 0))
    limit  = int(request.GET.get("limit", 12))  # <- İSTEDİĞİN KADAR
    items = GalleryItem.objects.order_by("-created_at")[offset:offset+limit]
    data = [{
        "type": i.content_type,
        "title_tr": i.title_tr,
        "title_en": i.title_en,
        "image": i.image.url if i.image else None,
        "youtube": i.youtube_embed(),
        "youtube_thumbnail": i.youtube_thumbnail,
    } for i in items]
    return JsonResponse(data, safe=False)


from .forms import GalleryItemForm
def gallery_manager_view(request, item_id=None):
    """
    Eğer item_id varsa -> update işlemi
    Eğer item_id yoksa -> create işlemi
    """
    if item_id:
        item = get_object_or_404(GalleryItem, id=item_id)
    else:
        item = None

    if request.method == "POST":
        form = GalleryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            if item:
                messages.success(request, "Galeri içeriği başarıyla güncellendi ✅")
            else:
                messages.success(request, "Yeni galeri içeriği eklendi ✅")
            return redirect("gallery_manager")  # urls.py’de bu adı vereceğiz
    else:
        form = GalleryItemForm(instance=item)

    items = GalleryItem.objects.order_by("-created_at")  # listeleme için

    return render(request, "websitemanager/gallerymanager.html", {
        "form": form,
        "items": items,
        "item_id": item_id,
    })






def asansorfren_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/frensistem.html")




def atlas_overload_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/atlasoverload.html")




def horusphotocell_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/fotosel.html")




def switchsystems_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/switchsistemleri.html")




def zemin_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/zemin.html")



def fan_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/fan.html")



def paten_view(request):
    """
    Liftkeys Atlas Aşırı Yük Sistemi blog yazısını render eder.
    """
    return render(request, "preview/previewblog/paten.html")



def solid_view(request):
    """
    Liftkeys Solid Makina blog yazısını render eder.
    """
    return render(request, "preview/previewblog/solid.html")




def kupeste_view(request):
    """
    Liftkeys Küpeşte blog yazısını render eder.
    """
    return render(request, "preview/previewblog/kupeste.html")



def takozlar_view(request):
    """
    Liftkeys Takozlar blog yazısını render eder.
    """
    return render(request, "preview/previewblog/takozlar.html")
    