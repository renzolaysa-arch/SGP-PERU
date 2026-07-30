from django import forms
from django.contrib.auth.models import User
from .models import Inventory, CommentInventory, QualityTest, InventoryTheme, InventoryThematic, InventoryStatus, TypeFormatSampleData, TransferMediumSampleData, TagsSampleData, VariablesSampleData
from datetime import datetime
from .widgets import DatePickerInput

ORDER_CHOICES = (
    ('', 'Ordenar por:'),
    ('title', 'Nombre'),
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

class CreateInventoryForm(forms.ModelForm):

    inventory_theme_asociate = forms.ModelChoiceField(
        queryset=InventoryTheme.on_site.all(),
        required=False,
    )
    inventory_thematic_asociate = forms.ModelChoiceField(
        queryset=InventoryThematic.on_site.all(),
        required=False,
    )
    type_format_data_asociate = forms.ModelChoiceField(
        queryset=TypeFormatSampleData.on_site.all(),
        required=False,
    )
    transfer_medium_data_asociate = forms.ModelChoiceField(
        queryset=TransferMediumSampleData.on_site.all(),
        required=False,
    )
    tag_sample_data_asociate = forms.ModelMultipleChoiceField(
        queryset=TagsSampleData.on_site.all(),
        required=False,
    )
    variables_sample_data_asociate = forms.ModelMultipleChoiceField(
        queryset=VariablesSampleData.on_site.all(),
        required=False,
    )

    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = [
            "entity_provider",
            "site",
            "created_date",
            "modified_date"
        ]
        widgets = {
            'date_start_collection': DatePickerInput(format=('%Y-%m-%d'), attrs={'class': 'input-normal', 'required': True}),
            'date_finish_collection': DatePickerInput(format=('%Y-%m-%d'), attrs={'class': 'input-normal', 'required': True}),
            'date_load_field': DatePickerInput(format=('%Y-%m-%d'), attrs={'class': 'input-normal'}),
        }

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = CommentInventory
        fields= ["comment_text"]
        
        
class QualityTestForm(forms.ModelForm):
    class Meta:
        model = QualityTest
        fields = [
            "quality_question_1",
            "quality_question_2",
            "quality_question_3",
            "quality_question_4",
            "quality_question_5",
        ]

        widgets = {
            'quality_question_1': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True, 'data_quest': 1}),
            'quality_question_2': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True, 'data_quest': 2}),
            'quality_question_3': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True, 'data_quest': 3}),
            'quality_question_4': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True, 'data_quest': 4}),
            'quality_question_5': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True, 'data_quest': 5}),
        }