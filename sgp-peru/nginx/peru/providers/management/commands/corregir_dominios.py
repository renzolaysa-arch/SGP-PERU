import re

from django.core.management.base import BaseCommand
from django.db import transaction

from providers.models import ProviderEntity


VALID_DOMAIN = re.compile(r'^(?!www\.)[a-z0-9-]+(\.[a-z0-9-]+)+$')


class Command(BaseCommand):
    help = (
        "Corrige el dominio de las entidades proveedoras del sitio actual que tienen una pagina web "
        "en lugar del dominio de correo, tomando el dominio de su correo de contacto (campo mail). "
        "Sin --aplicar solo muestra los cambios."
    )

    def add_arguments(self, parser):
        parser.add_argument('--aplicar', action='store_true', help='Guarda los cambios en la base de datos.')

    def handle(self, *args, **options):
        entities = list(ProviderEntity.on_site.order_by('id'))
        taken = {e.domain.strip().lower(): e for e in entities if VALID_DOMAIN.match(e.domain.strip().lower())}
        proposed = {}
        rows = []

        for entity in entities:
            current = entity.domain.strip()
            if VALID_DOMAIN.match(current.lower()):
                continue
            mail = (entity.mail or '').strip().lower()
            suggestion = mail.rpartition('@')[2] if '@' in mail else ''
            if not VALID_DOMAIN.match(suggestion):
                rows.append((entity, current, '-', 'sin correo de contacto valido: corregir a mano'))
            elif suggestion in taken:
                rows.append((entity, current, suggestion,
                             'conflicto: ya lo usa "%s" (id %s); decidir a mano' % (taken[suggestion].name, taken[suggestion].id)))
            elif suggestion in proposed:
                rows.append((entity, current, suggestion,
                             'conflicto: tambien se propone para id %s; decidir a mano' % proposed[suggestion].id))
            else:
                proposed[suggestion] = entity
                rows.append((entity, current, suggestion, 'se corrige'))

        if not rows:
            self.stdout.write('Todas las entidades del sitio tienen un dominio valido.')
            return

        for entity, current, suggestion, status in rows:
            self.stdout.write('%s | %s | %s -> %s | %s' % (entity.id, entity.name, current, suggestion, status))

        to_fix = [(entity, suggestion) for entity, _, suggestion, status in rows if status == 'se corrige']
        if not options['aplicar']:
            self.stdout.write(self.style.WARNING(
                '\nSimulacion: se corregirian %d de %d entidades. Ejecute con --aplicar para guardar.' % (len(to_fix), len(rows))))
            return

        with transaction.atomic():
            for entity, suggestion in to_fix:
                ProviderEntity.objects.filter(pk=entity.pk).update(domain=suggestion)
        self.stdout.write(self.style.SUCCESS('\nSe corrigieron %d entidades.' % len(to_fix)))
