from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from currency_rates.exceptions import ExchangeRateNotFound


class ExchangeRateNotFoundRedirectMixin(View):
    """
    Catch the ExchangeRateNotFound exception and redirect to a form to manually input the rate.
    Usage:

    class ProductDetailView(
        ExchangeRateNotFoundRedirectMixin,
        DetailView,
    ):
       ...

    """

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
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
                + "?next="
                + request.get_full_path()
            )
