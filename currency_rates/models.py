import datetime
from datetime import date, timedelta
from functools import partialmethod

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .converters import get_rate


class Currency(models.Model):
    code = models.CharField(_("Code"), max_length=3, unique=True)
    name = models.CharField(_("Name"), max_length=50)
    symbol = models.CharField(_("Symbol"), max_length=1, blank=True, null=True)
    is_default = models.BooleanField(
        _("Default"), default=False, help_text=_("Make this the default currency.")
    )

    selling_rates: "QuerySet[ExchangeRate]"

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        ordering = ("code",)

    def __unicode__(self):
        return self.code

    def __str__(self):
        return self.code

    # def save(self, **kwargs):
    #     if self.is_default:
    #         try:
    #             default_currency = Currency.objects.get(is_default=True)
    #         except self.DoesNotExist:
    #             pass
    #         else:
    #             default_currency.is_default = False
    #             default_currency.save()
    #     super(Currency, self).save(**kwargs)

    def current_rate(self, to_currency):
        return self.get_rate(to_currency)

    def get_rate(self, to_currency, date=datetime.date.today()):
        try:
            rate = self.selling_rates.get(currency_bought=to_currency, date=date)
            if rate:
                return rate.rate
        except ExchangeRate.DoesNotExist:
            new_rate = ExchangeRate(
                currency_sold=self,
                currency_bought=to_currency,
                rate=get_rate(
                    from_currency=self.code, to_currency=to_currency.code, date=date
                ),
                date=date,
            )
            new_rate.save()
            return new_rate.rate

    def to_currency(self, value, currency, date=datetime.date.today()):
        """
        Convert an value in the current currency to the value in the given currency.
        """
        rate = self.get_rate(to_currency=currency, date=date)
        return value * rate
        # result = value / self.current_rate(to_currency=currency)
        # if not currency.is_default:
        #     result *= currency.current_rate(to_currency=currency)
        # return result

    # to_default = partialmethod(to_currency, default_currency())


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

    def is_past_due(self):
        return self.date < date.today() - timedelta(days=15)
