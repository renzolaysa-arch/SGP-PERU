from django.contrib import admin
from .models import NewsLetter
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"

class NewsLetterAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["mail"]
    list_display = ("mail", "site", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["mail"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


admin.site.register(NewsLetter, NewsLetterAdmin)
