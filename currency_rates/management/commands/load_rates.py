import datetime
import json
from decimal import Decimal
from urllib.request import urlopen

from currency_rates.models import Currency, ExchangeRate
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

CURRENT_RATES_URL = "http://openexchangerates.org/latest.json"


class Command(BaseCommand):
    help = "Get the current rates from %s" % CURRENT_RATES_URL

    def handle(self, *args, **options):

        app_id = getattr(settings, "OPENEXCHANGERATES_APP_ID", None)
        if not app_id:
            raise Exception("No OPENEXCHANGERATES_APP_ID defined in settings")

        base_currency = getattr(settings, "CURRENCY_RATES_DEFAULT_CODE", 'EUR')

        url = CURRENT_RATES_URL + "?app_id=" + app_id
        f = urlopen(url)
        data = json.loads(f.read())

        # USD is the default in OpenExchangeRates, so we don't need conversion
        if base_currency != "USD":
            base_currency_rate = Decimal(str(data['rates'][base_currency]))
            conversion = lambda x: Decimal(str(x)) / base_currency_rate
        else:
            conversion = lambda x: x

        date = datetime.date.fromtimestamp(data['timestamp'])

        ExchangeRate.objects.filter(date=date).delete()

        for code, rate in list(data['rates'].items()):
            try:
                currency = Currency.objects.get(code=code)
            except Currency.DoesNotExist:
                continue
            ExchangeRate.objects.create(
                currency=currency, date=date, rate=conversion(rate))
