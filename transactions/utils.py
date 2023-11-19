from decimal import Decimal

import requests
from django.conf import settings


# gets the latest available information regarding the bank communication protocol
# and saves in the server configuration when starting it
def get_banks_data():
    response = requests.get(settings.BANK_DOMAINS_URL)
    return response.json()


def calc_comission(amount, kind, reference):
    for k, v in reference:
        if amount < k:
            return amount * Decimal(v[kind]) / 100
