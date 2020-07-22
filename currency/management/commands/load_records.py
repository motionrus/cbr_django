import datetime
import logging

from django.core.management import BaseCommand
from django.utils.timezone import now

from currency.models import Currency, DateRecordCurrency

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=90)

    def handle(self, *args, **options):
        days = options['days']

        if not Currency.objects.all():
            logger.info("No one Currency in DB. Populating...")
            Currency.loads()

        date_1 = now().date() - datetime.timedelta(days=days)
        date_2 = now().date()

        for currency in Currency.objects.all():
            logger.info("Get rates for '{}'".format(currency.name))
            DateRecordCurrency.load_for_dates(date_1, date_2, currency)
