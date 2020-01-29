import json
import time
import urllib
from decimal import Decimal
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings

from currency_rates.management.commands import load_currencies, load_rates
from currency_rates.models import Currency, ExchangeRate, default_currency


class CurrencyModelTest(TestCase):
    def test_currency_unicode(self):

        currency = Currency(code="EUR", name="Euro")

        self.assertEqual(str(currency), "EUR")

    # def test_no_rates(self):

    #     currency = Currency(code="EUR", name="Euro")
    #     to_currency = Currency(code="USD", name="Dollar")

    #     self.assertEqual(currency.current_rate(to_currency), None)

    def test_rates_set(self):

        currency = Currency.objects.create(code="EUR", name="Euro")
        to_currency = Currency(code="USD", name="Dollar")
        to_currency.save()

        rate = ExchangeRate.objects.create(
            currency_sold=currency, currency_bought=to_currency, rate=Decimal("2.00")
        )

        self.assertEqual(
            currency.current_rate(to_currency=to_currency), Decimal("2.00")
        )
        self.assertEqual(currency.current_rate(to_currency=to_currency), rate.rate)

    def test_change_default(self):

        eur = Currency.objects.create(code="EUR", name="Euro", is_default=True)
        usd = Currency.objects.create(code="USD", name="Dollar", is_default=True)
        # reread eur, to get the chages
        eur = Currency.objects.get(pk=eur.id)
        self.assertFalse(eur.is_default)
        self.assertTrue(usd.is_default)

    def test_only_one_default(self):

        Currency.objects.create(code="EUR", name="Euro", is_default=True)
        Currency.objects.create(code="USD", name="Dollar", is_default=True)

        self.assertEqual(Currency.objects.filter(is_default=True).count(), 1)

    def test_to_default(self):
        usd = Currency.objects.create(code="USD", name="Dollar", is_default=True)
        zar = Currency.objects.create(code="ZAR", name="South African Rand")
        ExchangeRate.objects.create(
            currency_sold=zar, currency_bought=usd, rate=Decimal(".75")
        )

        self.assertEqual(zar.to_default(10), Decimal("7.50"))

    def test_to_currency(self):
        Currency.objects.create(code="USD", name="Dollar", is_default=True)
        zar = Currency.objects.create(code="ZAR", name="South African Rand")
        eur = Currency.objects.create(code="EUR", name="Euro")
        ExchangeRate.objects.create(
            currency_sold=eur, currency_bought=zar, rate=Decimal("10.00")
        )
        ExchangeRate.objects.create(
            currency_sold=zar, currency_bought=eur, rate=Decimal("0.75")
        )

        self.assertEqual(zar.to_currency(10, eur), Decimal("7.5"))


class RateModelTest(TestCase):
    def test_rates_unicode(self):

        currency = Currency.objects.create(code="EUR", name="Euro")
        rate = ExchangeRate.objects.create(
            currency_sold=currency, currency_bought=currency, rate=Decimal("1.00")
        )

        self.assertEqual(
            str(rate), "Exchange rate from EUR to EUR on 2020-01-29 is 1.00"
        )


class DefaultCurrencyTest(TestCase):
    def test_non_existent(self):
        default = default_currency()
        self.assertEqual(default, None)

    def test_select_default(self):
        Currency.objects.create(code="EUR", name="Euro")
        usd = Currency.objects.create(code="USD", name="Dollar", is_default=True)

        default = default_currency()
        self.assertEqual(default, usd)

    def test_select_eur(self):
        eur = Currency.objects.create(code="EUR", name="Euro")
        Currency.objects.create(code="USD", name="Dollar")

        default = default_currency()
        self.assertEqual(default, eur)


class LoadCurrenciesTest(TestCase):

    # command = load_currencies.Command()
    # data = {"EUR": "Euro", "USD": "US Dollar"}

    def test_load_currencies(self):
        out = StringIO()
        call_command("load_currencies", stdout=out)
        # self.assertIn('Expected output', out.getvalue())

        # with mock.patch("urllib.request.urlopen") as mock_urlopen:
        #     attrs = {"read.return_value": json.dumps(self.data)}
        #     mock_urlopen.return_value = mock.MagicMock(**attrs)
        #     self.command.execute()

        usd = Currency.objects.get(code="USD")
        self.assertEqual(usd.name, "United States Dollar")


class LoadRatesTest(TestCase):
    def test_rate_not_in_db(self):
        currency = Currency(code="EUR", name="Euro")
        currency.save()
        to_currency = Currency(code="USD", name="Dollar")
        to_currency.save()
        self.assertEqual(currency.to_currency(value=10, currency=to_currency), 11.005)


# class LoadRatesTest(TestCase):

#     # command = load_rates.Command()
#     # data = {"rates": {"EUR": "0.8", "USD": 1}, "timestamp": time.time()}

#     def test_load_rates(self):

#         # create currency
#         Currency.objects.create(code="USD")
#         Currency.objects.create(code="EUR")

#         out = StringIO()
#         call_command("load_rates", stdout=out)
#         # self.assertIn('Expected output', out.getvalue())

#         # with mock.patch("urllib.request.urlopen") as mock_urlopen:
#         #     attrs = {"read.return_value": json.dumps(self.data)}
#         #     mock_urlopen.return_value = mock.MagicMock(**attrs)
#         #     self.command.execute()

#         usd_rate = ExchangeRate.objects.get(currency__code="USD")
#         self.assertEqual(usd_rate.rate, Decimal("1.25"))

#         eur_rate = ExchangeRate.objects.get(currency__code="EUR")
#         self.assertEqual(eur_rate.rate, Decimal("1"))

#         self.assertEqual(ExchangeRate.objects.count(), 2)

#     @override_settings(CURRENCY_RATES_DEFAULT_CODE="USD")
#     def test_load_rates_usd_base(self):

#         # create currency
#         Currency.objects.create(code="USD")
#         Currency.objects.create(code="EUR")

#         out = StringIO()
#         call_command("load_rates", stdout=out)
#         # self.assertIn('Expected output', out.getvalue())

#         # with mock.patch("urllib.request.urlopen") as mock_urlopen:
#         #     attrs = {"read.return_value": json.dumps(self.data)}
#         #     mock_urlopen.return_value = mock.MagicMock(**attrs)
#         #     self.command.execute()

#         usd_rate = ExchangeRate.objects.get(currency__code="USD")
#         self.assertEqual(usd_rate.rate, Decimal("1"))

#         eur_rate = ExchangeRate.objects.get(currency__code="EUR")
#         self.assertEqual(eur_rate.rate, Decimal("0.8"))

#         self.assertEqual(ExchangeRate.objects.count(), 2)

#     def test_load_rates_ignore_non_existent(self):

#         # create currency
#         Currency.objects.create(code="USD")

#         out = StringIO()
#         call_command("load_rates", stdout=out)
#         # self.assertIn('Expected output', out.getvalue())

#         # with mock.patch("urllib.request.urlopen") as mock_urlopen:
#         #     attrs = {"read.return_value": json.dumps(self.data)}
#         #     mock_urlopen.return_value = mock.MagicMock(**attrs)
#         #     self.command.execute()

#         usd_rate = ExchangeRate.objects.get(currency__code="USD")
#         self.assertEqual(usd_rate.rate, Decimal("1.25"))

#         self.assertEqual(ExchangeRate.objects.count(), 1)

#     @override_settings(OPENEXCHANGERATES_APP_ID=None)
#     def test_load_rates_no_app_id_exception(self):

#         self.assertRaises(Exception, self.command.execute)
#         try:
#             self.command.execute()
#         except Exception as e:
#             self.assertIn("OPENEXCHANGERATES_APP_ID", str(e))
