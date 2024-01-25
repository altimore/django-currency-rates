import datetime
from decimal import Decimal

from rich.console import Console

from currency_rates.exceptions import APILimitReached, ExchangeRateNotFound

# from .alphavantage import get_rate as get_rate_alphavantage
from .currencyapicom import get_rate as get_rate_currencyapicom
from .exchangeratesapiio import get_rate as get_rate_exchangeratesapiio
from .exchangeratesorguk import get_rate as get_rate_exchangeratesorguk

console = Console()
"""
eventually for later
https://www.abstractapi.com/api/exchange-rate-api#pricing
https://currency.getgeoapi.com/currency-plans/
"""


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:
    # here we iterate throught the differents api to get the rate.
    try:
        rate = get_rate_exchangeratesapiio(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            date=date,
        )
    except (APILimitReached, TimeoutError):
        try:
            rate = get_rate_currencyapicom(
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                date=date,
            )
        except APILimitReached:
            # try:
            rate = get_rate_exchangeratesorguk(
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                date=date,
            )
            # except ExchangeRateNotFound:

    if rate:
        return rate
    else:
        raise Exception("No change rate found, please add new exchangerate provider.")


if __name__ == "__main__":
    from_currency = "EUR"
    to_currency = "MUR"
    date = datetime.datetime.fromisoformat("2022-01-01")

    amount = 1

    print("Testing differents providers for the Exchange rate APIs.")
    # print("Test data EUR->MUR on 01-01-2022")

    print(
        get_rate(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            date=date,
        )
    )

    # console.rule("[bold red]exchangeratesapi.io")
    # # print("exchangeratesapi.io")
    # print(
    #     get_rate_exchangeratesapiio(
    #         from_currency=from_currency,
    #         to_currency=to_currency,
    #         amount=amount,
    #         date=date,
    #     )
    # )

    # console.rule("[bold red]exchangeratesorguk")
    # # print("exchangeratesorguk")
    # print(
    #     get_rate_exchangeratesorguk(
    #         from_currency=from_currency,
    #         to_currency=to_currency,
    #         amount=amount,
    #         date=date,
    #     )
    # )

    # print("Alpha Vantage")
    # print(
    #     get_rate_alphavantage(
    #         from_currency=from_currency,
    #         to_currency=to_currency,
    #         amount=amount,
    #         date=date,
    #     )
    # )
