# from https://exchangeratesapi.io/documentation/

import datetime
from decimal import Decimal

import requests

EXCHANGERATESAPIIO_API_KEY = getattr(
    settings, "EXCHANGERATESAPIIO_API_KEY", "YOURAPIKEYHERE"
)


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    if type(date) == str:
        url += f"&date={date}"
    elif type(date) == datetime.datetime:
        url += f"&date={date.strftime('%Y-%m-%d')}"

    payload = {}
    headers = {"apikey": EXCHANGERATESAPIIO_API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.json()
    return Decimal(result["result"])


if __name__ == "__main__":
    # print(get_rate(from_currency="EUR", to_currency="USD"))
    print(get_rate(from_currency="MGA", to_currency="USD", date="2022-01-01"))
