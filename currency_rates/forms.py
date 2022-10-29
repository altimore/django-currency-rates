from django.forms import CharField, HiddenInput, ModelForm
from django.utils.translation import gettext as _

from currency_rates.models import ExchangeRate


class ExchangeRateForm(ModelForm):
    next = CharField(label=_("Next page URL"), max_length=255, widget=HiddenInput())

    class Meta:
        model = ExchangeRate
        fields = "__all__"
