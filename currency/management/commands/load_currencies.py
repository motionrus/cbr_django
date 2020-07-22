from django.core.management import BaseCommand
from currency.models import Currency
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """ python manage.py load_currencies """

    def handle(self, *args, **options):
        Currency.loads()

        logger.info('Done. Currencies was populated.')
