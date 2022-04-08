from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from utils.mixins import Select2InclusiveFiltering

from .models import Currency


class CurrencyWidget(ModelSelect2Widget):
    model = Currency
    search_fields = ["code__icontains", "name__icontains", "symbol__icontains"]


class MultipleCurrencyWidget(ModelSelect2MultipleWidget):
    model = Currency
    search_fields = ["code__icontains", "name__icontains", "symbol__icontains"]
