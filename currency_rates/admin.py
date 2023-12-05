from django.contrib import admin

from .models import Currency, ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_default")
    list_filter = ("is_default",)
    search_fields = ("code", "name")


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("currency_sold", "currency_bought", "date", "rate")
    list_filter = ("date",)
    search_fields = ("currency__code", "currency__name")
