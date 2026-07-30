from django.shortcuts import get_object_or_404
from users.models import Provider, Unit_Central, Functionary


def user_photo(request):
    user = request.user
    group = user.groups.values_list('name', flat=True).first()
    if group == 'Unidad Central':
        user_object = Unit_Central.objects.filter(user=user).first()
    elif group == 'Proveedor':
        user_object = Provider.objects.filter(user=user).first()
    elif group == 'Funcionario':
        user_object = Functionary.objects.filter(user=user).first()

    if 'user_object' in locals() and user_object:
        user_photo = user_object.profile_image

    return {
        "user_photo": user_photo if 'user_photo' in locals() else '',
    }
