from django.contrib import admin
from .models import Provider, Unit_Central, Functionary, AccessUserRRA
from .forms import ProviderForm, UniteCentralForm, FunctionaryForm
from django.contrib.sites.shortcuts import get_current_site

# Register your models here.


class ProviderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "entity_provider",
        "site",
        "created_date",
        "modified_date"
    ]
    list_filter = [
        "user",
        "identification_number",
    ]
    search_fields = [
        "user"
    ]
    form = ProviderForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class UnitCentralAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "site",
        "created_date",
        "modified_date"
    ]
    list_filter = [
        "user"
    ]
    search_fields = [
        "user"
    ]
    form = UniteCentralForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class FunctionaryAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "site",
        "created_date",
        "modified_date"
    ]
    list_filter = [
        "user"
    ]
    search_fields = [
        "user"
    ]
    form = FunctionaryForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class AccessUserRRAAdmin(admin.ModelAdmin):
    fields = ["inventory", "user", "date_access", "date_limit"]
    list_display = [
        "user",
        "site",
        "created_date",
        "modified_date"
    ]
    list_filter = ["created_date", "site", "inventory", "user"]
    search_fields = ["inventory"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


#admin.site.register(Provider, ProviderAdmin)
#admin.site.register(Unit_Central, UnitCentralAdmin)
#admin.site.register(Functionary, FunctionaryAdmin)
#admin.site.register(AccessUserRRA, AccessUserRRAAdmin)
