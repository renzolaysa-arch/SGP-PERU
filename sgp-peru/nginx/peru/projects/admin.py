from django.contrib import admin
from .models import Project, CategoryProject, ThemeProject, StateProject, TagsProject, RelatedStatistical
from inventory.models import Inventory
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class TagProjectAdmin(admin.ModelAdmin):
    fields = ["name_tag_project", "type_color_choice"]
    list_display = ("name_tag_project", "site",
                    "created_date", "modified_date")
    list_filter = ["name_tag_project", "created_date"]
    search_fields = ["name_tag_project"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class CategoryAdmin(admin.ModelAdmin):
    fields = ["name_category_project"]
    list_display = ("name_category_project", "site",
                    "created_date", "modified_date")
    list_filter = ["name_category_project", "created_date"]
    search_fields = ["name_category_project"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class RelatedStatisticalAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["name", "created_date"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class ThemeAdmin(admin.ModelAdmin):
    fields = ["name_theme_project"]
    list_display = ("name_theme_project", "site",
                    "created_date", "modified_date")
    list_filter = ["name_theme_project", "created_date"]
    search_fields = ["name_theme_project"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class StateAdmin(admin.ModelAdmin):
    fields = ["state_project"]
    list_display = ("state_project", "site", "created_date", "modified_date")
    list_filter = ["state_project", "created_date"]
    search_fields = ["state_project"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()

class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"

class ProjectAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["name", "objetive_project", "tag_project", "category_project", "area_in_charge", "related_statistical", "provider_any_project", "functionary_project", "theme_project", "state_project", "rraa_asociate", "sub_title", "description_uno", "image_project_desk", "image_project_mob", "author_cita_imagen",
              "description_dos", "cita_contenido", "author_cita_contenido", "image_left_project_desk", "image_left_project_mob", "author_cita_imagen_left", "image_right_project_desk", "image_right_project_mob",
              "author_cita_imagen_right", "description_tres", "youtube", "cita_youtube"]
    list_display = ("name", "category_project", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "category_project",
                   "state_project"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


admin.site.register(TagsProject, TagProjectAdmin)
admin.site.register(CategoryProject, CategoryAdmin)
admin.site.register(ThemeProject, ThemeAdmin)
admin.site.register(StateProject, StateAdmin)
admin.site.register(RelatedStatistical, RelatedStatisticalAdmin)
admin.site.register(Project, ProjectAdmin)
