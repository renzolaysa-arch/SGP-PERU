from .models import News, Tags
from providers.models import ProviderEntity
from inventory.models import Inventory
from django import forms
import django_filters

class MegaSearchRraa(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="Buscador",
        lookup_expr='icontains'
    )
    class Meta:
        model = Inventory
        fields = ['title']
        
class MegaSearchProvider(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Buscador",
        lookup_expr='icontains'
    )
    class Meta:
        model = ProviderEntity
        fields = ['name']

class NewFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="Buscador",
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Palabra clave'})
    )
    created_date = django_filters.DateFilter(
        field_name='created_date',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='contains',
        label='Fecha'

    )
    tag_asociate = django_filters.ModelMultipleChoiceFilter(
        queryset=Tags.on_site.all().distinct(),
        field_name="tag_asociate",
        widget=forms.SelectMultiple(),

    )

    class Meta:
        model = News
        fields = ['title', 'created_date', 'tag_asociate']
