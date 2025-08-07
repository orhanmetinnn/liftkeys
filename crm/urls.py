from django.urls import path
from . import views

urlpatterns = [
    path('employeecreate/', views.employee_manage_view, name='employee_create'),
    path('jobinfo/', views.jobinfo_view, name='jobinfo_edit'),
    path('api/employee/<int:employee_id>/', views.employee_detail_api, name='employee_detail_api'),
    path('report/employee/', views.report_employee, name='report_employee'),
]
