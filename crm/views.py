from django.shortcuts import render

# Create your views here.
import logging
logger = logging.getLogger('django')

# def test_view(request):
#     logger.warning("Bu bir uyarı mesajıdır.")
#     logger.error("Bu bir hata mesajıdır.")
#     return HttpResponse("Log test edildi.")


from django.shortcuts import render, redirect
from .forms import EmployeeForm , JobInfoForm  # Formu içeri aktar
from django.contrib import messages 

def main_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Çalışan başarıyla kaydedildi.')
            return redirect('employee_create')  
        else:
            messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
    else:
        form = EmployeeForm()
    
    return render(request, 'crmemployee.html', {'form': form})




def jobinfo_view(request):
    if request.method == 'POST':
        formjobinfo = JobInfoForm(request.POST, request.FILES)
        if formjobinfo.is_valid():
            formjobinfo.save()
            messages.success(request, 'Çalışan başarıyla kaydedildi.')
            return redirect('jobinfo_edit')  # yönlendirme adresini ihtiyacına göre güncelle
        else:
            messages.error(request, 'Formda hatalar var. Lütfen düzeltin.')
    else:
        formjobinfo = JobInfoForm()  # ← burada doğru form nesnesi oluşturulmalı

    return render(request, 'crmjobinfo.html', {'formjobinfo': formjobinfo})








