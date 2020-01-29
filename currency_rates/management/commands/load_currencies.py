import json
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand

from currency_rates.models import Currency

CURRENCIES_URL = "http://openexchangerates.org/currencies.json"


class Command(BaseCommand):
    help = "Load currencies from %s" % CURRENCIES_URL

    def handle(self, **options):

        f = urllib.request.urlopen(CURRENCIES_URL)
        currencies = json.loads(f.read())

        for code, name in currencies.items():
            Currency.objects.get_or_create(code=code, defaults={"name": name})
