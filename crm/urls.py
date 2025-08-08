from django.urls import path
from . import views

urlpatterns = [
    path('employeecreate/', views.employee_manage_view, name='employee_create'),
    path('jobinfo/', views.jobinfo_view, name='jobinfo_edit'),
    path('api/employee/<int:employee_id>/', views.employee_detail_api, name='employee_detail_api'),
    path('report/employee/', views.report_employee, name='report_employee'),
    path('companies/manage/', views.company_manage_view, name='company_manage'),

    # Firma detay API'si (JSON döner)
    path('api/companies/<int:company_id>/', views.company_detail_api, name='company_detail_api'),
    path('api/sector/<int:sector_id>/', views.sector_detail_api, name='sector_detail_api'),

    # Country detay API
    path('api/country/<int:country_id>/', views.country_detail_api, name='country_detail_api'),
]
