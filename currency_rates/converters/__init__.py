import datetime
from decimal import Decimal

from currency_rates.exceptions import APILimitReached
from rich.console import Console

from exchangeratesapiio import get_rate as get_rate_exchangeratesapiio
from exchangeratesorguk import get_rate as get_rate_exchangeratesorguk

# from alphavantage import get_rate as get_rate_alphavantage

console = Console()


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
    except APILimitReached:
        rate = get_rate_exchangeratesorguk(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            date=date,
        )

    if rate:
        return rate
    else:
        raise Exception("No change rate found, please add new exchangerate provider.")


if __name__ == "__main__":
    from_currency = "EUR"
    to_currency = "MUR"
    date = datetime.datetime.fromisoformat("2022-01-01")

    amount = 1

    console.log(
        "Testing differents providers for the Exchange rate APIs.", log_locals=True
    )
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
