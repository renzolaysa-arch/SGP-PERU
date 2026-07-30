from django import forms
from .models import Project, CategoryProject, ThemeProject, StateProject, ProviderEntity, TagsProject, Inventory

ORDER_CHOICES = (
    ('', 'Ordenar por:'),
    ('name', 'Nombre'),
    ('-created_date', 'Fecha'),
)


class FilterOrderForm(forms.Form):
    order = forms.CharField(
        label="",
        required=False,
        widget=forms.Select(
            choices=ORDER_CHOICES
        ),
    )


class FilterProjectForm(forms.Form):
    name = forms.CharField(
        label="Buscador",
        required=False,
    )
    category_project = forms.ModelChoiceField(
        label="Categoría",
        queryset=CategoryProject.on_site.all(),
        required=False,
    )
    theme_project = forms.ModelChoiceField(
        label="Temática",
        queryset=ThemeProject.on_site.all(),
        required=False,
    )
    provider_project = forms.ModelChoiceField(
        label="Proveedor",
        queryset=ProviderEntity.on_site.all(),
        required=False,
    )
    state_project = forms.ModelChoiceField(
        label="Estado",
        queryset=StateProject.on_site.all(),
        required=False,
    )


class CreateProjectForm(forms.ModelForm):
    class TagProject(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    tag_project = TagProject(TagsProject.on_site.all())

    class ProvedorProject(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    provider_any_project = ProvedorProject(ProviderEntity.on_site.all())
    
    class CategorProject(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    category_project = CategorProject(CategoryProject.on_site.all())

    class ThematicProject(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    theme_project = ThematicProject(ThemeProject.on_site.all())

    class StatusProject(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    state_project = StatusProject(StateProject.on_site.all())

    class RraaProject(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    rraa_asociate = RraaProject(Inventory.on_site.all())
    class Meta:
        model = Project
        fields= [
            "name","objetive_project","tag_project", "category_project","area_in_charge","related_statistical","provider_any_project", "theme_project", "state_project", "rraa_asociate", "sub_title", "description_uno", "image_project_desk", "image_project_mob", "author_cita_imagen",
            "description_dos", "cita_contenido", "author_cita_contenido", "image_left_project_desk", "image_left_project_mob", "author_cita_imagen_left", "image_right_project_desk", "image_right_project_mob",
            "author_cita_imagen_right", "description_tres", "youtube", "cita_youtube" 
        ]
