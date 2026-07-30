from django.contrib import admin
from .models import Notification
from django.contrib.sites.shortcuts import get_current_site

# Register your models here.


class NotificationsAdmin(admin.ModelAdmin):
    fields = ["name", "sent_to", "module_from","message", "name_link", "link"]
    list_display = ("name", "sent_to", "site", "created_date", "modified_date")
    list_filter = ["created_date"]
    search_fields = ["name"]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


#admin.site.register(Notification, NotificationsAdmin)
