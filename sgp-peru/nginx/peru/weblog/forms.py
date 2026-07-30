from django import forms
from django.contrib.auth.models import User
from .models import ThemeThread, CommentThread
from django.core.exceptions import ValidationError

class CreateThemeThreadForm(forms.ModelForm):
    class Meta:
        model = ThemeThread
        fields= ["name_thread", "content_thread"]

class CreateCommentThreadForm(forms.ModelForm):
    class Meta:
        model = CommentThread
        fields= ["threadt_to_comment","commentary", "functionary_commented"]