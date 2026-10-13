from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from .models import Functionary, Provider, Unit_Central, AccessUserRRA, Inventory
from providers.models import ProviderEntity
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from demand.widgets import DatePickerInput
from datetime import datetime
import re
import django_filters


class ProviderForm(forms.ModelForm):

    class NameProviders(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    user = NameProviders(User.objects.filter(
        groups__name='Proveedor'), label="Usuario")
    
    class EntityProvider(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    entity_provider = EntityProvider(ProviderEntity.on_site.all())
    
    class Meta:
        model = Provider
        fields = [
            "user",
            "document_type",
            "identification_number",
            "entity_provider",
            "valid_data",
            "profile_image",
        ]


class UniteCentralForm(forms.ModelForm):
    class NameUniteCentral(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    user = NameUniteCentral(User.objects.filter(
        groups__name='Unidad Central'), label="Usuario")

    class Meta:
        model = Unit_Central
        fields = [
            "user",
            "profile_image"
        ]


class FunctionaryForm(forms.ModelForm):
    class NameFunctionary(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    user = NameFunctionary(User.objects.filter(
        groups__name='Funcionario'), label="Usuario")

    class Meta:
        model = Functionary
        fields = [
            "user",
            "profile_image",
        ]


class CreateProvider(forms.Form):
    name = forms.CharField(
        label="Nombre"
    )
    last_name = forms.CharField(
        label="Apellido"
    )
    document_type = forms.CharField(
        label="Tipo de identificacion",
        widget=forms.Select(choices=Provider.DOCUMENT_TYPE_CHOICES),
    )
    identification_number = forms.CharField(
        label="Numero de identificacion"
    )
    email = forms.EmailField(
        label="Correo electronico"
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(),

    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(),
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        required=True,
    )

    def clean(self):
        email = self.cleaned_data["email"]
        password_confirm = self.cleaned_data["password_confirm"]
        password = self.cleaned_data["password"]

        largo = re.compile(r'.{8,}')
        digito = re.compile(r'\d+')
        letra_may = re.compile(r'[A-Z]+')
        letra_min = re.compile(r'[a-z]+')

        validaciones = [(largo, "largo menor que ocho"),
                        (digito, "no tiene digitos"),
                        (letra_min, "no tiene letras minúsculas"),
                        (letra_may, "no tiene letras mayúsculas")]

        for validacion, mensaje in validaciones:
            if not validacion.search(password):
                self.add_error('password', ValidationError(
                    {mensaje}))

        if password != password_confirm:
            self.add_error('password', ValidationError(
                "Las contraseñas no coinciden"))
        elif User.objects.filter(username=email):
            self.add_error('email', ValidationError("El usuario ya existe"))


class loginUser(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput()
    )
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    remember_me = forms.BooleanField(
        required=False,
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.DEBUG:
            self.fields.pop('captcha', None)


class UpdateProvider(forms.ModelForm):

    class EntityProvider(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    entity_provider = EntityProvider(ProviderEntity.on_site.all())
 
    profile_image = forms.ImageField(
        label='Imagen de perfil',
        help_text='Las imágenes debe ser exactamente de 150x150 píxeles'
    )
    name = forms.CharField(
        label="Nombre",
        required=True,
    )
    last_name = forms.CharField(
        label="Apellido",
        required=True,
    )
    document_type = forms.CharField(
        label="Tipo de identificacion",
        required=True,
        widget=forms.Select(choices=Provider.DOCUMENT_TYPE_CHOICES),
    )
    identification_number = forms.CharField(
        label="Numero de identificacion",
        required=True,
    )
    email = forms.EmailField(
        label="Correo electronico",
        required=True,
    )
    is_active = forms.BooleanField(
        label='Activo',
        required=False
    )
    valid_data = forms.BooleanField(
        label='Data Verificada',
        required=False
    )
    class Meta:
        model = Provider
        fields = '__all__' 
        exclude = [
            "site",
            "created_date",
            "modified_date"
        ]

class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "is_active",
        ]


class EditProfileUnitCentral(forms.ModelForm):
    name = forms.CharField(
            label="Nombre",
            required=True,
        )
    last_name = forms.CharField(
            label="Apellido",
            required=True,
        )
    email = forms.EmailField(
        label="Correo electronico",
        required=True,
    )
    is_active = forms.BooleanField(
        label='Activo',
        required=False
    )
    class Meta:
        model = Unit_Central
        fields = [
            "profile_image",
        ]


class EditProfileProvider(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            "profile_image",
            "document_type",
            "identification_number",
        ]


class EditProfileFunctionary(forms.ModelForm):
    name = forms.CharField(
            label="Nombre",
            required=True,
        )
    last_name = forms.CharField(
            label="Apellido",
            required=True,
        )
    email = forms.EmailField(
        label="Correo electronico",
        required=True,
    )
    is_active = forms.BooleanField(
        label='Activo',
        required=False
    )
    class Meta:
        model = Functionary
        fields = [
            "profile_image",
        ]


class AccessUserRRAForm(forms.ModelForm):
    class AccessRraa(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    user = AccessRraa(Functionary.on_site.all())

    class Register(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.__str__

    inventory = Register(Inventory.on_site.all())
    class Meta:
        model = AccessUserRRA
        fields = '__all__'
        exclude = [
            "site",
            "created_date",
            "modified_date"
        ]
        widgets = {
            'date_access': DatePickerInput(attrs={'class': 'input-normal', 'required': True, 'min': datetime.now().strftime("%Y-%m-%d")}),
            'date_limit': DatePickerInput(attrs={'class': 'input-normal', 'required': True, 'min': datetime.now().strftime("%Y-%m-%d")}),
        }
