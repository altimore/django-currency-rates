import json
import urllib.request, urllib.error, urllib.parse
from django.core.management.base import NoArgsCommand
from currency_rates.models import Currency

CURRENCIES_URL = "http://openexchangerates.org/currencies.json"


class Command(NoArgsCommand):
        help = "Load currencies from %s" % CURRENCIES_URL

        def handle_noargs(self, **options):

            f = urllib.request.urlopen(CURRENCIES_URL)
            currencies = json.loads(f.read())

            for code, name in currencies.items():
                Currency.objects.get_or_create(code=code, defaults={'name': name})
