from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "Info_App"

urlpatterns = [
    path('',views.index,name="index"),
    path('home',views.home,name="home"),
    path('pdf_report_create',views.pdf_report_create,name='pdf_report_create'),
    path('submit_cainfo',views.submit_cainfo,name="submit_cainfo"),
    path('validate_no',views.validate_no,name="validate_no"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
