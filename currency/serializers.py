from rest_framework import serializers
from currency.models import Currency, DateRecordCurrency
from django.core import exceptions
import datetime


class DateRecordCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = DateRecordCurrency
        fields = [
            "date",
            "value",
        ]


class CurrencySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def filter_instance(self, instance):
        request = self.context['request']
        date = request.query_params.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))

        try:
            record = instance.currencies.filter(date=date)
            if record:
                return instance.currencies.filter(date=date).first()
        except exceptions.ValidationError as err:
            raise serializers.ValidationError(err.messages)

        return None

    def get_value(self, instance: Currency):
        filter_instance = self.filter_instance(instance)
        return filter_instance.value if filter_instance else None

    def get_date(self, instance: Currency):
        filter_instance = self.filter_instance(instance)
        return filter_instance.date if filter_instance else None

    class Meta:
        model = Currency
        fields = [
            "code",
            "num_code",
            "char_code",
            "nominal",
            "name",
            "value",
            "date"
        ]



