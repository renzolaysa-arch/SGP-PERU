from .models import Project, CategoryProject, ThemeProject, StateProject, ProviderEntity, TagsProject
from django import forms
import django_filters


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="",
        lookup_expr='icontains',
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=CategoryProject.on_site.all().distinct(),
        field_name="category_project",
        widget=forms.CheckboxSelectMultiple(),
        label="Categoría",
    )
    theme = django_filters.ModelChoiceFilter(
        queryset=ThemeProject.on_site.all().distinct(),
        field_name="name_theme_project",
        widget=forms.Select(),
    )
    status = django_filters.ModelMultipleChoiceFilter(
        queryset=StateProject.on_site.all().distinct(),
        field_name="state_project",
        widget=forms.CheckboxSelectMultiple(),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=TagsProject.on_site.all().distinct(),
        field_name="tag_project",
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Project
        fields = ['name', 'category_project', 'theme_project', 'state_project', 'tag_project']

