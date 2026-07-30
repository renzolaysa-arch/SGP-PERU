from django.contrib import admin
from .models import ThemeThread, CommentThread
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"

class ThreadAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["name_thread", "content_thread", "user_functionary_created"]
    list_display = ("name_thread", "created_date", "modified_date")
    list_filter = ["name_thread", "site"]
    search_fields = ["name_thread"]

class CommentAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["commentary", "threadt_to_comment", "functionary_commented"]
    list_display = ("commentary", "threadt_to_comment", "created_date", "modified_date")
    list_filter = ["commentary", "site"]
    search_fields = ["commentary"]

#admin.site.register(ThemeThread, ThreadAdmin)
#admin.site.register(CommentThread, CommentAdmin)