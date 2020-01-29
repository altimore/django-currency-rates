import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from forex_python.converter import CurrencyRates

from alpha_vantage.foreignexchange import ForeignExchange


def default_currency():
    try:
        return Currency.objects.get(is_default=True)
    except Currency.DoesNotExist:
        pass

    DEFAULT_CODE = getattr(settings, "CURRENCY_RATES_DEFAULT_CODE", "EUR")
    try:
        return Currency.objects.get(code=DEFAULT_CODE)
    except Currency.DoesNotExist:
        pass

    return None


def get_rate(from_currency, to_currency, date):
    try:
        c = CurrencyRates()
        return c.get_rate(from_currency, to_currency.code, date)
    except RatesNotAvailableError:

        fx = ForeignExchange(key="K1GJWM9EPXNN4E0N")

        print(
            fx.get_currency_exchange(
                from_currency=self.code, to_currency=to_currency.code
            )
        )

    return rate


class Currency(models.Model):
    code = models.CharField(_("Code"), max_length=3, unique=True)
    name = models.CharField(_("Name"), max_length=50)
    symbol = models.CharField(_("Symbol"), max_length=1, blank=True, null=True)
    is_default = models.BooleanField(
        _("Default"), default=False, help_text=_("Make this the default currency.")
    )

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        ordering = ("code",)

    def __unicode__(self):
        return self.code

    def __str__(self):
        return self.code

    def save(self, **kwargs):
        if self.is_default:
            try:
                default_currency = Currency.objects.get(is_default=True)
            except self.DoesNotExist:
                pass
            else:
                default_currency.is_default = False
                default_currency.save()
        super(Currency, self).save(**kwargs)

    def current_rate(self, to_currency):
        return self.get_rate(to_currency)

    def get_rate(self, to_currency, date=datetime.date.today()):
        try:
            rate = (
                self.selling_rates.filter(currency_bought=to_currency)
                .latest("date")
                .rate
            )
            return rate
        except ExchangeRate.DoesNotExist:
            new_rate = ExchangeRate(
                currency_sold=self,
                currency_bought=to_currency,
                rate=get_rate(self.code, to_currency.code, date),
                date=date,
            )
            new_rate.save()
            return new_rate.rate

    def to_default(self, value):
        """
        Convert a value in the current currency to the value in the default currenty.
        """
        return self.to_currency(value, default_currency())

    def to_currency(self, value, currency, date=datetime.date.today()):
        """
        Convert an value in the current currency to the value in the given currency.
        """
        return value * self.get_rate(to_currency=currency, date=date)
        # result = value / self.current_rate(to_currency=currency)
        # if not currency.is_default:
        #     result *= currency.current_rate(to_currency=currency)
        # return result


class ExchangeRate(models.Model):
    currency_sold = models.ForeignKey(
        Currency, related_name="selling_rates", on_delete=models.CASCADE
    )
    currency_bought = models.ForeignKey(
        Currency, related_name="purchase_rates", on_delete=models.CASCADE
    )

    date = models.DateField(_("Date"), default=datetime.date.today)
    rate = models.DecimalField(_("Rate"), max_digits=12, decimal_places=6)
    created = models.DateTimeField(_("Created"), auto_now=True)

    class Meta:
        verbose_name = _("Exchange rate")
        verbose_name_plural = _("Exchange rates")
        unique_together = ("currency_sold", "currency_bought", "date")
        ordering = ("-date", "currency_sold__code", "currency_bought__code")

    def __str__(self):
        return f"Exchange rate from {self.currency_sold} to {self.currency_bought} on {self.date} is {self.rate}"
