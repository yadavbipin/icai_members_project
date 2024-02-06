from django.urls import path
from . import views
app_name = "Info_App"

urlpatterns = [
    # path('',views.index,name="index"),
    path('home',views.home,name="home"),
    # path('pdf_report_create',views.pdf_report_create,name='pdf_report_create'),
    path('submit_cainfo',views.submit_cainfo,name="submit_cainfo"),
    path('',views.validate_no,name="validate_no"),
    path('edit_existing_cainfo/<int:ca_id>.<int:random_no>.<int:mem_no>',views.edit_existing_cainfo,name="edit_existing_cainfo"),
    path('existing_info_table',views.existing_info_table,name="existing_info_table"),

]
