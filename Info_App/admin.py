from django.contrib import admin
from .models import Personal_Info,form_submission
from import_export.admin import ImportExportModelAdmin


# Register your models here.
@admin.register(form_submission)

@admin.register(Personal_Info)
class ViewAdmin(ImportExportModelAdmin):
    pass
