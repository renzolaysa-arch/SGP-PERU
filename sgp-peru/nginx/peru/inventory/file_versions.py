"""Persist file replacements with an append-only version history."""
from pathlib import PurePosixPath
from uuid import uuid4
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from users.models import AccessUserRRA, Provider
from .models import Inventory, InventoryFileVersion


def can_view_history(user, inventory):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.groups.filter(name='Unidad Central').exists():
        return True
    if user.groups.filter(name='Proveedor').exists() and Provider.objects.filter(user=user, entity_provider_id=inventory.entity_provider_id, site_id=inventory.site_id).exists():
        return True
    today = timezone.localdate()
    return AccessUserRRA.objects.filter(
        user__user=user, inventory=inventory, site_id=inventory.site_id,
    ).filter(Q(date_access__isnull=True) | Q(date_access__lte=today)).filter(
        Q(date_limit__isnull=True) | Q(date_limit__gte=today)
    ).exists()


def save_with_history(form, user, entity_provider=None):
    with transaction.atomic():
        item = form.save(commit=False)
        old = Inventory.objects.select_for_update().filter(pk=item.pk).first() if item.pk else None
        if old and old.file_example_sample_data:
            InventoryFileVersion.objects.get_or_create(
                inventory=old, file=old.file_example_sample_data.name,
                defaults={'original_name': PurePosixPath(old.file_example_sample_data.name).name, 'uploaded_at': None},
            )
        uploaded = form.files.get('file_example_sample_data')
        original_name = uploaded.name if uploaded else None
        if uploaded:
            uploaded.name = uuid4().hex + PurePosixPath(original_name).suffix.lower()
            item.file_example_sample_data.name = uploaded.name
        elif old and form.cleaned_data.get('file_example_sample_data') is not False:
            item.file_example_sample_data = old.file_example_sample_data.name
        if entity_provider is not None:
            item.entity_provider = entity_provider
        item.save()
        form.save_m2m()
        if uploaded:
            InventoryFileVersion.objects.create(
                inventory=item, file=item.file_example_sample_data.name,
                original_name=original_name, uploaded_by=user, uploaded_at=timezone.now(),
            )
        return item
