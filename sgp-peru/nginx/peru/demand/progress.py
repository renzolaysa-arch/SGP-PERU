"""Progress is based on deliveries, not duplicate preparation rows or visited pages."""
from .models import Transfers, Preparations


def preparation_progress(preparation, transfer):
    deliveries = Transfers.on_site.filter(transfer=transfer) if transfer else Transfers.on_site.none()
    rows = Preparations.on_site.filter(preparation=preparation, transfer__in=deliveries)
    total = deliveries.count()
    completed_ids = rows.filter(finalize=True).values_list('transfer_id', flat=True).distinct()
    completed = deliveries.filter(pk__in=completed_ids).count()
    pending = deliveries.exclude(pk__in=completed_ids)
    if total and completed == total:
        status = 'fi'
    elif not rows.exists():
        status = 'ini'
    elif pending.exists() and rows.filter(transfer__in=pending, date_revision__isnull=False).values('transfer_id').distinct().count() == pending.count():
        status = 're'
    else:
        status = 'pr'
    return {
        'total': total, 'completed': completed, 'pending': total - completed,
        'percent': (completed * 100) // total if total else 0,
        'status': status,
        'pending_deliveries': list(pending.values_list('number_deliveries', flat=True)),
    }


def sync_preparation_state(preparation):
    transfer = preparation.demand.transfer
    status = preparation_progress(preparation, transfer)['status']
    if preparation.demand_process != status:
        preparation.demand_process = status
        preparation.save(update_fields=['demand_process'])
