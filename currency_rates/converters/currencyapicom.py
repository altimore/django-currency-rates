# from https://currencyapi.com/docs/latest

import datetime
import logging
from decimal import Decimal

import requests
from django.conf import settings
from requests.exceptions import JSONDecodeError as RequestsJSONDecodeError

from currency_rates.exceptions import APILimitReached

logger = logging.getLogger(__name__)

# EXCHANGERATESAPIIO_API_KEY = getattr(
#     settings, "EXCHANGERATESAPIIO_API_KEY", "YOURAPIKEYHERE"
# )

CURRENCYAPICOM_API_KEY = "ILqiDS7dQWUegqM8bj5ybjDVNlSnfKYxMiju0Jnj"
HISTORICAL_REQUEST_URL = "https://api.currencyapi.com/v3/historical"
LATEST_RATE_URL = "https://api.currencyapi.com/v3/latest"


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:
    REQUEST_URL = LATEST_RATE_URL

    if date != datetime.date.today():
        REQUEST_URL = HISTORICAL_REQUEST_URL

    url = f"{REQUEST_URL}?apikey={CURRENCYAPICOM_API_KEY}&base_currency={from_currency}&currencies={to_currency}"

    # print("!", date, type(date))
    if type(date) == str:
        url += f"&date={date}"
    elif type(date) == datetime.datetime:
        url += f"&date={date.strftime('%Y-%m-%d')}"

    logger.debug(f"Trying url {url}")
    payload = {}
    # headers = {"apikey": EXCHANGERATESAPIIO_API_KEY}
    headers = {}

    # print("#", url)
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 429:
        raise APILimitReached(
            "You have hit your rate limit or your monthly limit. For more requests please upgrade your plan (opens new window)."
        )

    try:
        result = response.json()
    except RequestsJSONDecodeError:
        raise Exception(
            f"Cannot decode JSON from the url {url} the response is : {response}"
        )

    # print("*", result)
    return Decimal(result["data"][to_currency]["value"])


if __name__ == "__main__":
    print(get_rate(from_currency="EUR", to_currency="USD"))
    # print(get_rate(from_currency="MGA", to_currency="USD", date="2022-01-01"))
