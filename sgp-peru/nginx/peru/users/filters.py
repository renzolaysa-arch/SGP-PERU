import django_filters
from .models import AccessUserRRA
from inventory.models import Inventory
from users.models import Functionary
from django import forms


class AccessUserRRAFilter(django_filters.FilterSet):
    inventory = django_filters.ModelChoiceFilter(
        queryset=Inventory.on_site.all().distinct(),
        field_name="inventory",
        widget=forms.Select(),
    )
    
    user = django_filters.ModelChoiceFilter(
        queryset=Functionary.on_site.all().distinct(),
        field_name="user",
        widget=forms.Select(),
    )
    
    class Meta:
        model = AccessUserRRA
        fields = ['inventory','user']
