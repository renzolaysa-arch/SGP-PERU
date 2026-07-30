from django.contrib import admin
from .models import Banner, Benefit, Gallery, MenuItem, Tags, menuList, TDivipola, Divipola, Documents, News, Letter, Vocabulary, FAQs, Visitor, Testimony
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site


class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"


class BannerAdmin(admin.ModelAdmin):
    fields = ["title", "sub_title", "background", "description",
              "url_name", "url_link", "youtube", "image"]
    list_display = ("title", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class BenefitAdmin(admin.ModelAdmin):
    fields = ["title", "description", "icon"]
    list_display = ("title", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TDivipolaAdmin(admin.ModelAdmin):
    fields = ["name", "sigla", "parent"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class DivipolaAdmin(admin.ModelAdmin):
    fields = ["name", "sigla", "parent", "tdivipola"]
    list_display = ("name", "tdivipola", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class MenuItemInLine(admin.StackedInline):
    model = MenuItem
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    fields = ["titleMenu", "Menu_Choice"]
    inlines = [MenuItemInLine]
    list_display = ("titleMenu", "site")
    list_filter = ["site"]
    search_fields = ["titleMenu"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class DocumentsAdmin(admin.ModelAdmin):
    fields = ["title", "document", "assigned_to",
              "copy_to", "requires_approval"]
    list_display = ["title", "site", "assigned_to",
                    "approved", "requires_approval"]
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class GalleryItemInLine(admin.StackedInline):
    model = Gallery
    extra = 3


class TagsAdmin(admin.ModelAdmin):
    fields = ["name_tag", "type_color_choice"]
    list_display = ("name_tag", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name_tag"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "tag_asociate", "type_choice", "previous_description", "author", "photo_author", "sub_title", "description_uno", "youtube",
                  "cita_youtube", "description_dos", "cita_noticia", "main_image_new_desk", "main_image_new_mob"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_site = Site.objects.get_current()
        self.fields['tag_asociate'].queryset = self.fields['tag_asociate'].queryset.filter(
            site=current_site)


class NewsAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    form = NewsForm
    inlines = [GalleryItemInLine]
    list_display = ("title", "site", "author", "type_choice",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class LettersAdmin(admin.ModelAdmin):
    fields = ["name_letter"]
    list_display = ("name_letter", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name_letter"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class VocabularyAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["letter", "word", "meaning"]
    list_display = ("letter", "word", "site", "created_date", "modified_date")
    search_fields = ["word"]


class FaqsAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["name_question_faqs", "response_faqs"]
    list_display = ("name_question_faqs", "site",
                    "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name_question_faqs"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class VisitorAdmin(admin.ModelAdmin):
    fields = ["ip_user", "rol_visited", "url_visited",
              "type_model_visited", "id_model_visited"]
    list_display = ("ip_user", "site", "created_date")
    list_filter = ["created_date", "site"]
    search_fields = ["ip_user"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TestimonyAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["logo", "title", "video_image",
              "video_testimony", "description_testimony"]
    list_display = ("title", "site", "created_date")
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


admin.site.register(Testimony, TestimonyAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Benefit, BenefitAdmin)
admin.site.register(menuList, MenuAdmin)
admin.site.register(TDivipola, TDivipolaAdmin)
admin.site.register(Divipola, DivipolaAdmin)
#admin.site.register(Documents, DocumentsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Letter, LettersAdmin)
admin.site.register(Vocabulary, VocabularyAdmin)
admin.site.register(FAQs, FaqsAdmin)
#admin.site.register(Visitor, VisitorAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)
