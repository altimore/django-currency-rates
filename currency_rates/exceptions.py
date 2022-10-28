import datetime


class ExchangeRateNotFound(Exception):
    """Exception raised for errors in the rate inquired.

    Attributes:
        currency_sold
        currency_bought
        date
    """

    def __init__(
        self,
        currency_bought,
        currency_sold,
        date=datetime.date.today(),
        message="Currency exchange rate not found",
    ):
        self.currency_bought = currency_bought
        self.currency_sold = currency_sold
        self.date = date
        self.message = message

        super().__init__()

    def __str__(self):
        return f"Error when inquiring the rate of exchange from {self.currency_sold} to {self.currency_bought} on the {self.date} {self.message}."


class APILimitReached(Exception):
    pass
