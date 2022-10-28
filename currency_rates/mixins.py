from django.http import HttpResponseRedirect
from django.urls import reverse

from currency_rates.exceptions import ExchangeRateNotFound


class ExchangeRateNotFoundRedirectMixin(object):
    def get(self, request, *args, **kwargs):
        try:
            super.get(request, *args, **kwargs)
        except ExchangeRateNotFound as e:
            return HttpResponseRedirect(
                reverse(
                    "change-rate-create",
                    kwargs={
                        "from_currency": e.currency_sold,
                        "to_currency": e.currency_bought,
                        "date": e.date,
                    },
                )
            )
