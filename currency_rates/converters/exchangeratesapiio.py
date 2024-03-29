# from https://exchangeratesapi.io/documentation/

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

EXCHANGERATESAPIIO_API_KEY = "OL5dkSwVprfzUxCzJ2c66Oohd4H6XG0q"


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:
    logger.info(
        f"Trying to get rate from {from_currency} to {to_currency} on {date} with ExchangeRatesAPI.io"
    )
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    if type(date) == str:
        url += f"&date={date}"
    elif type(date) == datetime.datetime:
        url += f"&date={date.strftime('%Y-%m-%d')}"

    logger.debug(f"Trying url {url}")
    payload = {}
    headers = {"apikey": EXCHANGERATESAPIIO_API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 524 or status_code == 522:
        raise TimeoutError()
    try:
        result = response.json()
    except RequestsJSONDecodeError:
        raise OSError(
            f"Cannot decode JSON from the url {url} the response is : {response}"
        )

    try:
        if (
            result["message"]
            == "You have exceeded your daily/monthly API rate limit. Please review and upgrade your subscription plan at https://promptapi.com/subscriptions to continue."
        ):
            raise APILimitReached(result["message"])
    except KeyError:
        # there is no error message
        pass

    return Decimal(result["result"])


if __name__ == "__main__":
    # print(get_rate(from_currency="EUR", to_currency="USD"))
    print(get_rate(from_currency="MGA", to_currency="USD", date="2022-01-01"))
