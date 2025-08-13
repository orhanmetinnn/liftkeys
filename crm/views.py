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
from .models import Employee , Sector,Country,Product,Category,Product
from .forms import EmployeeForm, EmployeeUpdateForm,UpdateCompanyForm,ProductForm,CategoryForm,UpdateCategoryForm,UpdateProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


logger = logging.getLogger('django')
"""
Personel Alanı
"""



# Logger oluştur
logger = logging.getLogger(__name__)

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

        # CREATE işlemi
        if 'create_submit' in request.POST:
            logger.info("Yeni çalışan ekleme isteği alındı.")
            form_create = EmployeeForm(request.POST, request.FILES, prefix='create')
            if form_create.is_valid():
                try:
                    form_create.save()
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
                    form_update = EmployeeUpdateForm(request.POST, request.FILES, instance=selected_employee, prefix='update')
                    if form_update.is_valid():
                        form_update.save()
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

def jobinfo_view(request):
    # Form nesneleri başta boş oluşturuluyor
    formjobinfo = JobInfoForm()
    formtitle = TitlePersonelForm()
    formdepartment = DepartmentForm()
    formworklocation = WorkLocationForm()

    if request.method == 'POST':
        print("POST request alındı")
        if 'submit_jobinfo' in request.POST:
            formjobinfo = JobInfoForm(request.POST)
            if formjobinfo.is_valid():
                formjobinfo.save()
                messages.success(request, 'Çalışan başarıyla kaydedildi.')
                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'İş bilgisi formunda hata var.')

        elif 'submit_title' in request.POST:
            print("burası çalıştı")
            formtitle = TitlePersonelForm(request.POST)
            if formtitle.is_valid():
                formtitle.save()
                messages.success(request, 'Unvan başarıyla eklendi.')
                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'Unvan formunda hata var.')

        elif 'submit_department' in request.POST:
            formdepartment = DepartmentForm(request.POST)
            if formdepartment.is_valid():
                formdepartment.save()
                messages.success(request, 'Departman başarıyla eklendi.')
                return redirect('jobinfo_edit')
            else:
                messages.error(request, 'Departman formunda hata var.')

        elif 'submit_worklocation' in request.POST:
            formworklocation = WorkLocationForm(request.POST)
            if formworklocation.is_valid():
                formworklocation.save()
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






def report_employee(request):

    employees = Employee.objects.select_related('job_info_as_employee', 'job_info_as_employee__title', 'job_info_as_employee__department', 'job_info_as_employee__work_location', 'job_info_as_employee__manager').all()

    total_employees = employees.count()

    # Departman bazlı dağılım
    dept_distribution = JobInfo.objects.values('department__name').annotate(count=Count('id')).order_by('-count')

    # Cinsiyet dağılımı
    gender_distribution = employees.values('gender').annotate(count=Count('id'))

    # Çalışma tipi dağılımı
    employment_type_distribution = JobInfo.objects.values('employment_type').annotate(count=Count('id'))

    # Yıllara göre işe başlama sayısı (örnek: son 5 yıl)
    from django.db.models.functions import ExtractYear
    from django.utils.timezone import now
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

def company_manage_view(request):
    logger.info("Firma yönetim sayfası açıldı.")
    company_list = None
    form_create = CompanyForm(prefix='create')
    form_update = CompanyForm(prefix='update')
    selected_company = None
    ulke_list=None
    sector_list=None
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

        # CREATE işlemi
        if 'create_submit' in request.POST:
            logger.info("Yeni firma ekleme isteği alındı.")
            form_create = CompanyForm(request.POST, prefix='create')
            if form_create.is_valid():
                try:
                    form_create.save()
                    logger.info("Yeni firma başarıyla kaydedildi.")
                    messages.success(request, 'Firma başarıyla kaydedildi.')
                    return redirect('company_manage')  # URL adını kendine göre değiştir
                except Exception as e:
                    logger.exception("Yeni firma kaydedilirken hata oluştu.")
                    messages.error(request, 'Firma kaydedilirken bir hata oluştu.')
            else:
                logger.warning(f"Yeni firma formu geçersiz. Hatalar: {form_create.errors}")
                messages.error(request, 'Yeni firma formunda hata var.')

        # UPDATE işlemi
        elif 'update_submit' in request.POST:
            company_id = request.POST.get('update_company_id')
            logger.debug(f"Güncelleme için gelen firma ID: {company_id}")

            if company_id:
                try:
                    selected_company = Company.objects.get(pk=company_id)
                    form_update = UpdateCompanyForm(request.POST, instance=selected_company, prefix='update')
                    if form_update.is_valid():
                        form_update.save()
                        logger.info(f"Firma (ID: {company_id}) bilgileri güncellendi.")
                        messages.success(request, 'Firma bilgileri başarıyla güncellendi.')
                        return redirect('company_manage')  # URL adını kendine göre değiştir
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_update.errors}")
                        messages.error(request, 'Güncelleme formunda hata var.')
                except Company.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen firma bulunamadı. ID: {company_id}")
                    messages.error(request, 'Güncellenecek firma bulunamadı.')
                except Exception as e:
                    logger.exception(f"Firma (ID: {company_id}) güncellenirken beklenmeyen bir hata oluştu.")
                    messages.error(request, 'Güncelleme sırasında bir hata oluştu.')
            else:
                logger.error("Güncelleme isteğinde firma ID bilgisi eksik.")
                messages.error(request, 'Firma ID bilgisi eksik.')


        elif 'create_country_submit' in request.POST:
            logger.info("Yeni ülke ekleme isteği alındı.")
            form_country = CountryForm(request.POST, prefix='country')
            if form_country.is_valid():
                try:
                    form_country.save()
                    logger.info("Yeni ülke başarıyla kaydedildi.")
                    messages.success(request, 'Ülke başarıyla kaydedildi.')
                    return redirect('company_manage')  # URL adını kendine göre değiştir
                except Exception as e:
                    logger.exception("Yeni ülke kaydedilirken hata oluştu.")
                    messages.error(request, 'Ülke kaydedilirken hata oluştu.')
            else:
                logger.warning(f"Yeni ülke formu geçersiz. Hatalar: {form_country.errors}")
                messages.error(request, 'Ülke formunda hata var.')

        elif 'update_country_submit' in request.POST:
            country_id = request.POST.get('update_country_id')
            logger.debug(f"Güncelleme için gelen ülke ID: {country_id}")
            if country_id:
                try:
                    selected_country = Country.objects.get(pk=country_id)
                    form_country = UpdateCountryForm(request.POST, instance=selected_country, prefix='update')
                    if form_country.is_valid():
                        form_country.save()
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

        # SECTOR FORM İŞLEMİ
        elif 'create_sector_submit' in request.POST:
            logger.info("Yeni sektör ekleme isteği alındı.")
            form_sector = SectorForm(request.POST, prefix='sector')
            if form_sector.is_valid():
                try:
                    form_sector.save()
                    logger.info("Yeni sektör başarıyla kaydedildi.")
                    messages.success(request, 'Sektör başarıyla kaydedildi.')
                    return redirect('company_manage')
                except Exception as e:
                    logger.exception("Yeni sektör kaydedilirken hata oluştu.")
                    messages.error(request, 'Sektör kaydedilirken hata oluştu.')
            else:
                logger.warning(f"Yeni sektör formu geçersiz. Hatalar: {form_sector.errors}")
                messages.error(request, 'Sektör formunda hata var.')

        elif 'update_sector_submit' in request.POST:
            sector_id = request.POST.get('update_sector_id')
            logger.debug(f"Güncelleme için gelen sektör ID: {sector_id}")
            if sector_id:
                try:
                    selected_sector = Sector.objects.get(pk=sector_id)
                    form_sector = UpdateSectorForm(request.POST, instance=selected_sector, prefix='update')
                    if form_sector.is_valid():
                        form_sector.save()
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
        'selected_country': selected_country if 'selected_country' in locals() else None,

        'form_create_sector': SectorForm(prefix='sector'),
        'form_update_sector': UpdateSectorForm(prefix='update'),
        'selected_sector': selected_sector if 'selected_sector' in locals() else None,
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




def directory_company_update(request):
    try:
        if request.method == 'POST':
            form = DirectoryCompanyForm(request.POST)  # Yeni kayıt
            if form.is_valid():
                form.save()
                messages.success(request, "Bilgiler başarıyla kaydedildi.")
                logger.info("DirectoryCompany yeni kaydı oluşturuldu.")
                return redirect('directory_company_update')
            else:
                messages.error(request, "Formda hatalar var, lütfen kontrol edin.")
                logger.warning(f"DirectoryCompany form doğrulama hatası: {form.errors}")
        else:
            form = DirectoryCompanyForm()  # Boş form

        all_companies_list = DirectoryCompany.objects.all().order_by('-created_at')

        # Sayfalama
        page = request.GET.get('page', 1)
        paginator = Paginator(all_companies_list, 10)  # Sayfa başına 10 kayıt

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


def product_create_update(request):
    try:
        catagory_list = Category.objects.all()
        logger.debug(f"{catagory_list.count()} katagori listelendi.")
    except Exception as e:
        logger.exception("katagori listesi alınırken hata oluştu.")
        messages.error(request, 'katagori listesi alınırken bir hata oluştu.')
        catagory_list = []

    try:
        urun_list = Product.objects.all()
        logger.debug(f"{urun_list.count()} ürün listelendi.")
    except Exception as e:
        logger.exception("ürün listesi alınırken hata oluştu.")
        messages.error(request, 'ürün listesi alınırken bir hata oluştu.')
        urun_list = []


    if request.method == 'POST':
        if 'create_catagory_submit' in request.POST:
            form_create=CategoryForm(request.POST,prefix='create')
            if form_create.is_valid():
                form_create.save()
                logger.info("Yeni katagori başarıyla kaydedildi.")
                messages.success(request, 'Katagori başarıyla kaydedildi.')
                return redirect('product_list')  # URL adını kendine göre değiştir
        elif 'update_catagory_submit' in request.POST:
            category_id = request.POST.get('update_catagory_id')
            logger.debug(f"Güncelleme için gelen kategori ID: {category_id}")
            if category_id:
                try:
                    selected_category = Category.objects.get(pk=category_id)
                    form_update = UpdateCategoryForm(request.POST, instance=selected_category, prefix='update')
                    if form_update.is_valid():
                        form_update.save()
                        logger.info(f"Kategori (ID: {category_id}) başarıyla güncellendi.")
                        messages.success(request, 'Kategori başarıyla güncellendi.')
                        return redirect('product_list')  # Burayı kendi yönlendirmene göre değiştir
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_update.errors}")
                        messages.error(request, 'Kategori güncelleme formunda hata var.')
                except Category.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen kategori bulunamadı. ID: {category_id}")
                    messages.error(request, 'Güncellenecek kategori bulunamadı.')
                except Exception as e:
                    logger.exception(f"Kategori (ID: {category_id}) güncellenirken hata oluştu: {e}")
                    messages.error(request, 'Kategori güncelleme sırasında hata oluştu.')
            else:
                logger.error("Kategori güncelleme isteğinde ID eksik.")
                messages.error(request, 'Kategori ID bilgisi eksik.')


        elif 'create_product_button' in request.POST:
            print("burasi çalıştı")
            form_create = ProductForm(request.POST, request.FILES, prefix='create')  # <-- request.FILES ekledik
            if form_create.is_valid():
                form_create.save()
                logger.info("Yeni ürün başarıyla kaydedildi.")
                messages.success(request, 'Ürün başarıyla kaydedildi.')
                return redirect('product_list')
            else:
                print(form_create.errors)  # <-- Burada hata mesajlarını yazdırabilirsiniz      



        elif 'update_product_submit' in request.POST:
            product_id = request.POST.get('update_product_id')
            logger.debug(f"Güncelleme için gelen ürün ID: {product_id}")

            if product_id:
                try:
                    selected_product = Product.objects.get(pk=product_id)
                    form_update = UpdateProductForm(
                        request.POST,
                        request.FILES,
                        instance=selected_product,
                        prefix='update'
                    )

                    if form_update.is_valid():
                        form_update.save()
                        logger.info(f"Ürün (ID: {product_id}) başarıyla güncellendi.")
                        messages.success(request, 'Ürün başarıyla güncellendi.')
                        return redirect('product_list')  # kendi sayfana göre değiştir
                    else:
                        logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_update.errors}")
                        messages.error(request, 'Ürün güncelleme formunda hata var.')

                except Product.DoesNotExist:
                    logger.warning(f"Güncellenmek istenen ürün bulunamadı. ID: {product_id}")
                    messages.error(request, 'Güncellenecek ürün bulunamadı.')

                except Exception as e:
                    logger.exception(f"Ürün (ID: {product_id}) güncellenirken hata oluştu: {e}")
                    messages.error(request, 'Ürün güncelleme sırasında hata oluştu.')
            else:
                logger.error("Ürün güncelleme isteğinde ID eksik.")
                messages.error(request, 'Ürün ID bilgisi eksik.')

    context = {
        'form': ProductForm(prefix='create'),
        'UpdateProductForm':UpdateProductForm(prefix='update'),
        'formcatogryupdate':UpdateCategoryForm(prefix='update'),
        'formcreatecatagory':CategoryForm(prefix='create'),
        'catagory_list':catagory_list,
        'urun_list':urun_list,
    }
    return render(request, 'urunler/uruncreateandupdate.html', context)

    #     form = ProductForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('product_list')  # Ürün listesine yönlendir (url adına göre düzenle)
    # else:
    #     pass




def catogory_detail_api(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    data = {
        'id': category.id,
        'name': category.name,
    }
    return JsonResponse(data)



def product_detail_api(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    data = {
        'id': product.id,
        'name': product.name,
        'website_image_url': product.website_image.url if product.website_image else None,
        'mobile_image_url': product.mobile_image.url if product.mobile_image else None,
        'features': product.features,
        'stock_code': product.stock_code,
        'categories': list(product.categories.values_list('id', flat=True)),
        'description': product.description,
        'price': str(product.price),  # Decimal JSON’da string olmalı
        'is_active': product.is_active,
        'warranty_period': product.warranty_period,
    }
    return JsonResponse(data)