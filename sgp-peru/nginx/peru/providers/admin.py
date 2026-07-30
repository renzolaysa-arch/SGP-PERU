from django.contrib import admin
from .models import ProviderEntity, ProviderStatus, ProviderTopic, ProviderCategory, ProviderType, ProviderDocuments, ProviderSector, Stage
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class StageDocumentAdmin(admin.ModelAdmin):
    fields = ["name_stage"]
    list_display = ["name_stage", "modified_date"]
    list_filter = ["name_stage"]
    search_fields = ["name_stage"]


class ProviderDocumentsInLine(admin.StackedInline):
    model = ProviderDocuments
    extra = 3

class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"

class ProviderEntityAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["name", "identification_number", "description", "sector", "type", "mision", "sicode", "territorial_level", "web", "mail", "telephone", "location",
              "agent_mame", "agent_position", "official_name", "official_position", "official_mail", "official_telephone", "image", "domain", "status", "category", "topic"]
    list_display = ("name", "site", "created_date", "modified_date")
    inlines = [ProviderDocumentsInLine]
    list_filter = ["created_date", "site"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class ProviderStatusAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["name"]


class ProviderSectorAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["name"]


class ProviderCategoryAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["name"]


class ProviderTopicAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["name"]


class ProviderTypeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["name"]

#admin.site.register(ProviderEntity, ProviderEntityAdmin)
admin.site.register(ProviderStatus, ProviderStatusAdmin)
admin.site.register(ProviderCategory, ProviderCategoryAdmin)
admin.site.register(ProviderTopic, ProviderTopicAdmin)
admin.site.register(ProviderType, ProviderTypeAdmin)
admin.site.register(ProviderSector, ProviderSectorAdmin)
#admin.site.register(Stage, StageDocumentAdmin)
