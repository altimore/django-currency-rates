import datetime
import logging
import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from currency_rates.exceptions import ExchangeRateNotFound

# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("sodibur_portal." + __name__)


class ExchangeRatesOrgUk:
    from_currency_code: str
    to_currency_code: str
    date: datetime.date

    def __init__(
        self, from_currency_code, to_currency_code, date=datetime.date.today()
    ):
        self.from_currency_code = from_currency_code
        self.to_currency_code = to_currency_code
        self.date = date

    def get_rate(self):
        if not self.date:
            self.date = datetime.date.today()

        logger.info(
            f"Trying to get rate from {self.from_currency_code} to {self.to_currency_code} on {self.date} with ExchangeRates.org.uk"
        )
        url = f"https://www.exchangerates.org.uk/{self.from_currency_code}-{self.to_currency_code}-spot-exchange-rates-history-{self.date.year}.html"

        html_code = requests.get(url).text

        soup = BeautifulSoup(html_code, "html.parser")

        monthly_tag = soup.find("h3", string=self.date.strftime("%B %Y"))
        logger.debug(monthly_tag)
        monthly_table = monthly_tag.next_sibling.next_sibling
        logger.debug(monthly_table)

        # print(monthly_tag, monthly_table)
        logger.debug(
            f"Looking for /{self.from_currency_code}-{self.to_currency_code}-{self.date.strftime('%d_%m_%Y')}-exchange-rate-history.html"
        )
        daily_rate_link_tag = monthly_table.find(
            href=f"/{self.from_currency_code}-{self.to_currency_code}-{self.date.strftime('%d_%m_%Y')}-exchange-rate-history.html"
        )
        try:
            change_rate_text = daily_rate_link_tag.parent.previous_sibling.text
        except:
            raise ExchangeRateNotFound(
                currency_sold=self.from_currency_code,
                currency_bought=self.to_currency_code,
                date=self.date,
            )

        self.rate = re.findall(r"[-+]?[0-9]*\.[0-9]+$", change_rate_text)[-1]

        return Decimal(self.rate)

    def __str__(self):
        return f"<ExchangeRatesOrgUk {self.from_currency_code} {self.to_currency_code} {self.date}>"


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:
    rate = ExchangeRatesOrgUk(from_currency, to_currency, date)
    return rate.get_rate()


if __name__ == "__main__":
    date = datetime.date(2019, 12, 19)
    date = datetime.date.today()
    rate = ExchangeRatesOrgUk("MUR", "USD", date)
    print(date, rate.get_rate())
