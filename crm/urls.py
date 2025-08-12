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
    path('directorycompany/update/', views.directory_company_update, name='directory_company_update'),
    path('urunlercompany/', views.product_create_update, name='product_list'),
    path('catogory_detail_api/<int:category_id>/',views.catogory_detail_api,name='catogory_detail_api')
]







# if 'create_submit' in request.POST:
#     logger.info("Yeni firma ekleme isteği alındı.")
#     form_create = CompanyForm(request.POST, prefix='create')
#     if form_create.is_valid():
#         try:
#             form_create.save()
#             logger.info("Yeni firma başarıyla kaydedildi.")
#             messages.success(request, 'Firma başarıyla kaydedildi.')
#             return redirect('company_manage')  # URL adını kendine göre değiştir
#         except Exception as e:
#             logger.exception("Yeni firma kaydedilirken hata oluştu.")
#             messages.error(request, 'Firma kaydedilirken bir hata oluştu.')
#     else:
#         logger.warning(f"Yeni firma formu geçersiz. Hatalar: {form_create.errors}")
#         messages.error(request, 'Yeni firma formunda hata var.')



# elif 'update_country_submit' in request.POST:
#             country_id = request.POST.get('update_country_id')
#             logger.debug(f"Güncelleme için gelen ülke ID: {country_id}")
#             if country_id:
#                 try:
#                     selected_country = Country.objects.get(pk=country_id)
#                     form_country = UpdateCountryForm(request.POST, instance=selected_country, prefix='update')
#                     if form_country.is_valid():
#                         form_country.save()
#                         logger.info(f"Ülke (ID: {country_id}) başarıyla güncellendi.")
#                         messages.success(request, 'Ülke başarıyla güncellendi.')
#                         return redirect('company_manage')
#                     else:
#                         logger.warning(f"Güncelleme formu geçersiz. Hatalar: {form_country.errors}")
#                         messages.error(request, 'Ülke güncelleme formunda hata var.')
#                 except Country.DoesNotExist:
#                     logger.warning(f"Güncellenmek istenen ülke bulunamadı. ID: {country_id}")
#                     messages.error(request, 'Güncellenecek ülke bulunamadı.')
#                 except Exception as e:
#                     logger.exception(f"Ülke (ID: {country_id}) güncellenirken hata oluştu.")
#                     messages.error(request, 'Ülke güncelleme sırasında hata oluştu.')
#             else:
#                 logger.error("Ülke güncelleme isteğinde ID eksik.")
#                 messages.error(request, 'Ülke ID bilgisi eksik.')