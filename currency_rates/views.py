from django.urls import reverse
from django.views.generic import CreateView

from .forms import ExchangeRateForm
from .models import Currency, ExchangeRate


class ChangeRateCreateView(CreateView):
    model = ExchangeRate
    template_name = "currency_rates/exchange_rate_form.haml"
    form_class = ExchangeRateForm
    object = None

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get("from_currency"):
            self.from_currency = Currency.objects.get(code=kwargs["from_currency"])
        if kwargs.get("to_currency"):
            self.to_currency = Currency.objects.get(code=kwargs["to_currency"])
        if kwargs.get("date"):
            self.date = kwargs["date"]

        self.return_url = request.GET.get("next", None)

        self.initial = {
            "currency_sold": self.from_currency,
            "currency_bought": self.to_currency,
            "date": self.date,
        }
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            next = form.cleaned_data.get("next")
            if next:
                self.return_url = next

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.return_url
        # if self.return_url:
        #     return self.return_url
        # else:
        #     return reverse("portal-dashboard")

    def get_initial(self):
        initial = self.initial.copy()
        if self.return_url:
            initial["next"] = self.return_url
        return initial
