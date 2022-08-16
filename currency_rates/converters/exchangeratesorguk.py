import datetime
import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup


class ExchangeRatesOrgUk(object):
    from_currency_code: str
    to_currency_code: str
    date: datetime.date

    def __init__(self, from_currency_code, to_currency_code, date):
        self.from_currency_code = from_currency_code
        self.to_currency_code = to_currency_code
        self.date = date

    def get_rate(self):
        url = f"https://www.exchangerates.org.uk/{self.from_currency_code}-{self.to_currency_code}-spot-exchange-rates-history-{self.date.year}.html"

        html_code = requests.get(url).text

        soup = BeautifulSoup(html_code, "html.parser")

        monthly_tag = soup.find("h3", string=self.date.strftime("%B %Y"))
        monthly_table = monthly_tag.next_sibling.next_sibling

        # print(monthly_tag, monthly_table)

        daily_rate_link_tag = monthly_table.find(
            href=f"/{self.from_currency_code}-{self.to_currency_code}-{self.date.strftime('%d_%m_%Y')}-exchange-rate-history.html"
        )
        change_rate_text = daily_rate_link_tag.parent.previous_sibling.text

        self.rate = re.findall(r"[-+]?[0-9]*\.[0-9]+$", change_rate_text)[-1]

        return Decimal(self.rate)


def get_rate(
    from_currency, to_currency, amount=1, date=datetime.date.today()
) -> Decimal:
    rate = ExchangeRatesOrgUk(from_currency, to_currency, date)
    return rate.get_rate()


if __name__ == "__main__":
    date = datetime.date(2019, 12, 19)
    rate = ExchangeRatesOrgUk("MUR", "USD", date)
