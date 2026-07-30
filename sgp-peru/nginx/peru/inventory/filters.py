from .models import Inventory, InventoryTheme, InventoryThematic
from providers.models import ProviderEntity
from django import forms
import django_filters

class InventoryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="Buscador",
        lookup_expr='icontains'
    )
    created_date = django_filters.DateFilter(
        field_name='created_date',
        widget= forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='contains',
        label='Fecha'
    )
    modified_date = django_filters.DateFilter(
        field_name='modified_date',
        widget= forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='contains',
        label='Fecha de publicación'
    )
    theme_inventory = django_filters.ModelChoiceFilter(
        queryset=InventoryTheme.on_site.all().distinct(),
        field_name="inventory_theme_asociate",
        widget=forms.Select(),
    )
    name_thematic_inventory = django_filters.ModelChoiceFilter(
        queryset=InventoryThematic.on_site.all().distinct(),
        field_name="inventory_thematic_asociate",
        widget=forms.Select(),
    )
    entity_provider = django_filters.ModelChoiceFilter(
        queryset=ProviderEntity.on_site.all().distinct(),
        field_name="entity_provider",
        widget=forms.Select(),
    )
    custody = django_filters.BooleanFilter(
        field_name="custody",
    )
    class Meta:
        model = Inventory
        fields = ['title', 'created_date', 'modified_date','entity_provider', 'theme_inventory', 'name_thematic_inventory', 'custody']