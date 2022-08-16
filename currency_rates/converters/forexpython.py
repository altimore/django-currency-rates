import datetime
from decimal import Decimal

from forex_python.converter import CurrencyRates, RatesNotAvailableError


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:

    c = CurrencyRates()
    rate = c.get_rate(from_currency, to_currency, date)
    return Decimal(rate)
