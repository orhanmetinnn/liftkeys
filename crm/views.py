from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Employee , JobInfo , TitlePersonel, Department, WorkLocation
# Create your views here.
import logging
logger = logging.getLogger('django')
from django.http import JsonResponse
# def test_view(request):
#     logger.warning("Bu bir uyarı mesajıdır.")
#     logger.error("Bu bir hata mesajıdır.")
#     return HttpResponse("Log test edildi.")


from django.shortcuts import render, redirect
from .forms import EmployeeForm , JobInfoForm ,TitlePersonelForm, DepartmentForm, WorkLocationForm,EmployeeUpdateForm  # Formu içeri aktar
from django.contrib import messages 
from django.db.models import Count

def employee_manage_view(request):
    employee_list = Employee.objects.all()
    form_create = EmployeeForm(prefix='create')
    form_update = EmployeeUpdateForm(prefix='update')
    selected_employee = None

    if request.method == 'POST':
        if 'create_submit' in request.POST:
            form_create = EmployeeForm(request.POST, request.FILES, prefix='create')
            if form_create.is_valid():
                form_create.save()
                messages.success(request, 'Çalışan başarıyla kaydedildi.')
                return redirect('employee_create')
            else:
                messages.error(request, 'Yeni çalışan formunda hata var.')

        elif 'update_submit' in request.POST:
            employee_id = request.POST.get('update_employee_id')
            print(f"Güncelleme için gelen çalışan ID: {employee_id}")
            if employee_id:
                try:
                    selected_employee = Employee.objects.get(pk=employee_id)
                    form_update = EmployeeUpdateForm(request.POST, request.FILES, instance=selected_employee, prefix='update')
                    if form_update.is_valid():
                        form_update.save()
                        messages.success(request, 'Çalışan bilgileri başarıyla güncellendi.')
                        return redirect('employee_create')
                    else:
                        messages.error(request, 'Güncelleme formunda hata var.')
                except Employee.DoesNotExist:
                    messages.error(request, 'Güncellenecek çalışan bulunamadı.')
            else:
                messages.error(request, 'Çalışan ID bilgisi eksik.')

    context = {
        'employee_list': employee_list,
        'form_create': form_create,
        'form_update': form_update,
        'selected_employee': selected_employee,
    }
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