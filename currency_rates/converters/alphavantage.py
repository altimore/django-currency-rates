import datetime
from decimal import Decimal

from alpha_vantage.foreignexchange import ForeignExchange


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:

    fx = ForeignExchange(key="K1GJWM9EPXNN4E0N")

    result, sthing = fx.get_currency_exchange_rate(
        from_currency=from_currency, to_currency=to_currency
    )
    # print(result["5. Exchange Rate"])
    return Decimal(result["5. Exchange Rate"])
