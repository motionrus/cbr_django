import datetime

from django.db import models, transaction, IntegrityError
from .utils import get_currencies_info, get_dynamic_rates, str_to_date
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class Currency(models.Model):
    """ Currency model """
    code = models.CharField(verbose_name='code', max_length=12, unique=True, db_index=True)
    num_code = models.SmallIntegerField(verbose_name='num code', blank=True, null=True, default=None)
    char_code = models.CharField(verbose_name='char code', max_length=3, blank=True, db_index=True, null=True,
                                 default=None)
    nominal = models.IntegerField(verbose_name='nominal', default=1)
    name = models.CharField(verbose_name='name', max_length=64)

    @classmethod
    def loads(cls):
        raw_currencies = get_currencies_info()
        for currency in raw_currencies:

            try:
                with transaction.atomic():
                    cls.objects.create(
                        code=currency.attrib['ID'],
                        num_code=currency.findtext('ISO_Num_Code') or None,
                        char_code=currency.findtext('ISO_Char_Code'),
                        nominal=currency.findtext('Nominal'),
                        name=currency.findtext('Name'),
                    )
            except IntegrityError as err:
                logger.warning('{} with id: {} is already populated. Skipping.'.format(
                        currency.findtext('EngName'),
                        currency.attrib['ID'])
                    )

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'currencies'


class DateRecordCurrency(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="currencies")
    date = models.DateField()
    value = models.DecimalField(verbose_name='value', max_digits=9, decimal_places=4)

    @classmethod
    def load_for_dates(cls, date_begin: datetime.datetime, date_end: datetime.datetime, currency: Currency):
        raw_rates = get_dynamic_rates(date_req1=date_begin, date_req2=date_end, currency_id=currency.code)

        for rate in raw_rates:
            with transaction.atomic():
                try:
                    cls.objects.get_or_create(
                        currency=currency,
                        date=str_to_date(rate.attrib['Date']).date(),
                        value=Decimal(rate.findtext('Value').replace(',', '.'))
                    )
                except IntegrityError:
                    logger.warning("Rate {} for {} already in db. Skipped.".format(
                        currency.name, str_to_date(rate.attrib['Date'])))

        return cls.objects.filter(currency=currency, date__gte=date_begin, date__lte=date_end)

    class Meta:
        verbose_name = 'Date record currency'
        verbose_name_plural = 'Date record currencies'
        constraints = [
            models.UniqueConstraint(fields=['currency', 'date'], name='unique currency of date')
        ]
