from django.contrib import admin
from .models import (
    DemandsCategories,
    DemandsStatus,
    Demands,
    KeyWords,
    ProviderDemand,
    Topic,
    Note,
    Reception,
    DemandsTheme,
    Transfer,
    Negotiation,
    Transfers,
    Channels,
    Preparation,
    Preparations,
    DocumentDefinitionObjetives,
    ParticipationDemand,
    Evaluation,
    Evaluations
)
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class NotesInLine(admin.StackedInline):
    fields = ["commentary"]
    model = Note
    extra = 3


class DemandsCategoriesAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]


class DemandsThemeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]


class DemandsStatusAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]

class CustomImportExportModelAdmin(ImportExportModelAdmin):
    from_encoding = "ISO-8859-1"
    to_encoding = "ISO-8859-1"

class DemandsAdmin(CustomImportExportModelAdmin, admin.ModelAdmin):
    fields = ["functionary", "inventory", "project", "title", "description", "use", "time", "product", "status", "category", "theme", "provider_entity", "topic", "key_words", "file_demand", "type",
              "finish_date", "process"]
    inlines = [NotesInLine]
    list_display = ("title", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["title"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class KeyWordsAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]


class TopicAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]


class ReceptionAdmin(admin.ModelAdmin):
    fields = [
        "demand", "demand_subprocess", "date_demand_validation",
        "date_verification_completeness", "status_demand_validation",
        "demand_process", "demand_assessment", "date_demand_notification",
        "date_tentative_presentation", "status_demand_notification",
        "comment", "date_demand_revision", "comment_revision",
        "date_demand_finalized", "time_demand_finalized", "comment_finalized",
        "punctual_need", "full_justification", "approval_instance",
    ]
    list_display = ("demand", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["demand"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TransferAdmin(admin.ModelAdmin):
    fields = ["demand", "demand_process"]
    list_display = ("demand", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["demand"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class NegotiationAdmin(admin.ModelAdmin):
    fields = [
        "demand", "demand_process",
        "demand_subprocess", "date_demand_validation",
        "date_definition_objetives",
        "date_scope_validate",
        "status_demand_negotiation",
        "date_revision",
        "date_finalize",
        "time_demand_finalized",
        "date_agreed",
        "time",
        "type_time",
        "date_agreement",
        "channel",
        "consideration",
        "meets_expectations",
        "required_documentation",
        "ready_sign",
    ]
    list_display = ("demand", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["demand"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class TransfersAdmin(admin.ModelAdmin):
    fields = [
        "transfer", "status_transfer",
        "number_deliveries", "date_delivery",
        "comment",
        "channel",
        "date_reviewed",
        "comment_review",
        "reviewed",
        "date_finalize",
        "comment_finalize",
        "finalize",
        "validate_preparation",
        "open_base",
        "expected_size",
        "meets_terms",
        "approve_reception_bd",
        "preparation",
    ]
    list_display = ("transfer", "status_transfer", "site",
                    "created_date", "modified_date")
    list_filter = ["status_transfer"]
    search_fields = ["transfer"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class ChannelsAdmin(admin.ModelAdmin):
    fields = [
        "title",
    ]
    list_display = ("title", "created_date", "modified_date")
    search_fields = ["title"]


class ProviderDemandAdmin(admin.ModelAdmin):
    fields = ["negotiation", "provider_entity",
              "status_demand", "status_record"]
    list_display = ("provider_entity", "site", "created_date", "modified_date")
    search_fields = ["negotiation"]


class PreparationAdmin(admin.ModelAdmin):
    exclude = [
        "site",
        "created_date",
        "modified_date"
    ]
    list_display = ("demand", "site", "created_date", "modified_date")
    search_fields = ["transfer"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()
    
class PreparationsAdmin(admin.ModelAdmin):
    exclude = [
        "site",
        "created_date",
        "modified_date"
    ]
    list_display = ("preparation", "transfer", "site", "created_date", "modified_date")
    search_fields = ["transfer"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class DocumentDefinitionObjetivesAdmin(admin.ModelAdmin):
    exclude = ['site']
    list_display = ("name", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class ParticipationDemandAdmin(admin.ModelAdmin):
    exclude = ['site']
    list_display = ("user", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["user.username"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class EvaluationAdmin(admin.ModelAdmin):
    fields = ["doc_evaluation",
              "date_finalize",
              "comment_finalize",
              "finalize",
              ]
    list_display = ("demand", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["demand"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


class EvaluationsAdmin(admin.ModelAdmin):
    fields = ["evaluation",
              "functionary",
              "date_notification",
              "frequency",
              "frequency_delivery",
              "frequency_date_delivery",
              "finish_date",
              "interview",
              "question_1",
              "question_2",
              "question_3",
              "question_4",
              "question_5",
              "question_6",
              "question_7",
              "question_8",
              "question_9",
              "question_10",
              "result",
              "evaluation_answer",
              ]
    list_display = ("evaluation", "site", "created_date", "modified_date")
    list_filter = ["created_date", "site"]
    search_fields = ["demand"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(site__id=get_current_site(request).id)
        return qs.on_site()


#admin.site.register(Demands, DemandsAdmin)
admin.site.register(KeyWords, KeyWordsAdmin)
admin.site.register(DemandsCategories, DemandsCategoriesAdmin)
admin.site.register(DemandsStatus, DemandsStatusAdmin)
admin.site.register(Topic, TopicAdmin)
#admin.site.register(Reception, ReceptionAdmin)
admin.site.register(DemandsTheme, DemandsThemeAdmin)
#admin.site.register(Transfer, TransferAdmin)
#admin.site.register(Negotiation, NegotiationAdmin)
#admin.site.register(ProviderDemand, ProviderDemandAdmin)
#admin.site.register(Transfers, TransfersAdmin)
admin.site.register(Channels, ChannelsAdmin)
#admin.site.register(Preparation, PreparationAdmin)
#admin.site.register(Preparations, PreparationsAdmin)
#admin.site.register(DocumentDefinitionObjetives,
#                    DocumentDefinitionObjetivesAdmin)
#admin.site.register(ParticipationDemand, ParticipationDemandAdmin)
#admin.site.register(Evaluation, EvaluationAdmin)
#admin.site.register(Evaluations, EvaluationsAdmin)
