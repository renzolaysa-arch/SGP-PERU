from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Documents, News, Testimony
from users.models import Functionary, Provider, Unit_Central, User
from inventory.models import Inventory
from django.apps import apps
from django.db import connections


def data_users_related():
    options_users = []
    modelo = apps.get_model('users', 'Provider')

    with connections['default'].cursor() as cursor:
        table_names = connections['default'].introspection.table_names()
        if modelo._meta.db_table in table_names:
            providers = Provider.on_site.all()
            unit_central = Unit_Central.on_site.all()
            functionary = Functionary.on_site.all()
            users = [
                providers,
                unit_central,
                functionary
            ]

            for provider in users:
                for item in provider:
                    options_users.append((item.user.id, item.user.username))

    return options_users


SEARCH_FOR = (
    ('inventario', 'Registros Administrativos - RRAA'),
    ('proveedor', 'Proveedores​'),
)


class FilterSearchForm(forms.Form):
    order = forms.CharField(
        label="",
        required=True,
        widget=forms.RadioSelect(
            choices=SEARCH_FOR
        ),
    )


class CommentDocumentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=CKEditorWidget(),
        required=False,
    )
    approved = forms.BooleanField(
        label='Aprobar',
        required=False
    )

    assigned_to = forms.CharField(
        label="Asignado A:",
        required=True,
        widget=forms.Select(choices=data_users_related()),
    )

    copy_to = forms.CharField(
        label="Copia A:",
        required=True,
        widget=forms.SelectMultiple(choices=data_users_related()),
    )

    class Meta:
        model = Documents
        fields = [
            'comment',
            'approved',
        ]

    def save(self, *args, **kwargs):
        m = super(NewDocumentForm, self).save(commit=False, *args, **kwargs)
        data = self.cleaned_data
        assigned_to = User.objects.get(id=data['assigned_to'])
        m.assigned_to = assigned_to
        m.save()
        return m


class NewDocumentForm(forms.ModelForm):
    document = forms.FileField()

    assigned_to = forms.CharField(
        label="Asignado A:",
        required=True,
        widget=forms.Select(choices=data_users_related()),
    )

    copy_to = forms.CharField(
        label="Copia A:",
        required=True,
        widget=forms.SelectMultiple(choices=data_users_related()),
    )

    class Meta:
        model = Documents
        fields = [
            "title",
            "document",
            "requires_approval"
        ]

    def save(self, *args, **kwargs):
        m = super(NewDocumentForm, self).save(commit=False, *args, **kwargs)
        data = self.cleaned_data
        assigned_to = User.objects.get(id=data['assigned_to'])
        m.assigned_to = assigned_to
        m.save()
        return m


class CreateTestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = ["user_testimony",
                  "title",
                  "video_testimony",
                  "description_testimony"
                  ]
