from django import forms
from .models import NewsLetter


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = [
            "mail",
            "terms"
        ]
        widgets = {
            'mail': forms.EmailInput(attrs={"placeholder": "Ej: Usuario@mail.com"}),
            'terms': forms.CheckboxInput(attrs={"required": "required"}),
        }
