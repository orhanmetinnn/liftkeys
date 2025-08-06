from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='employee_create'),
    path('jobinfo/', views.jobinfo_view, name='jobinfo_edit'),

]
