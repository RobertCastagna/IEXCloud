import requests


class IEXStock:
    def __init__(self, token, symbol):
        self.BASE_URL = 'https://sandbox.iexapis.com/v1'

        self.token = token
        self.symbol = symbol

    def get_logo(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_company_info(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_historical_prices(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/chart/1m?token={self.token}"
        r = requests.get(url)

        return r.json()
