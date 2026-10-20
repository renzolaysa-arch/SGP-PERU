from django.contrib import admin
from .file_versions import save_with_history
from .models import Inventory, InventoryStatus, InventoryTheme, InventoryThematic, CommentInventory, QualityTest
from .models import TypeFormatSampleData, TransferMediumSampleData, TagsSampleData, VariablesSampleData
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class InventoryThemeAdmin(admin.ModelAdmin):
    fields = ["name_theme_inventory"]
    list_display = ("name_theme_inventory", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name_theme_inventory"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class InventoryThematicAdmin(admin.ModelAdmin):
    fields = ["name_thematic_inventory"]
    list_display = ("name_thematic_inventory", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name_thematic_inventory"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TypeFormatSampleDataAdmin(admin.ModelAdmin):
    fields = ["type_format"]
    list_display = ("type_format", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["type_format"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TransferMediumSampleDataAdmin(admin.ModelAdmin):
    fields = ["transfer_medium"]
    list_display = ("transfer_medium", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["transfer_medium"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TagsSampleDataAdmin(admin.ModelAdmin):
    fields = ["tags_sample_data"]
    list_display = ("tags_sample_data", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["tags_sample_data"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class VariablesSampleDataAdmin(admin.ModelAdmin):
    fields = ["variables_sample_data"]
    list_display = ("variables_sample_data", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["variables_sample_data"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class InventoryStatusAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()

class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"

class InventoryAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):    
    exclude = ['site']
    list_display = ("title", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def save_model(self, request, obj, form, change):
        save_with_history(form, request.user)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class CommentInventoryAdmin(admin.ModelAdmin):
    exclude = ['site']
    list_display = ("comment_text", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["comment_text"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class QualityTestAdmin(admin.ModelAdmin):
    exclude = ['site']
    list_display = ("inventory", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


admin.site.register(TypeFormatSampleData, TypeFormatSampleDataAdmin)
admin.site.register(TransferMediumSampleData, TransferMediumSampleDataAdmin)
admin.site.register(TagsSampleData, TagsSampleDataAdmin)
admin.site.register(VariablesSampleData, VariablesSampleDataAdmin)
admin.site.register(InventoryTheme, InventoryThemeAdmin)
admin.site.register(InventoryThematic, InventoryThematicAdmin)
admin.site.register(InventoryStatus, InventoryStatusAdmin)
admin.site.register(Inventory, InventoryAdmin)
#admin.site.register(CommentInventory, CommentInventoryAdmin)
#admin.site.register(QualityTest, QualityTestAdmin)
