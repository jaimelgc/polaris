from decimal import Decimal
import random
import string

import requests
from django.conf import settings


def random_alphanum(pin_lenght):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=pin_lenght))


def get_banks_data():
    response = requests.get(settings.BANK_DOMAINS_URL)
    return response.json()


def calc_comission(amount, kind, reference):
    for k, v in reference:
        if amount < k:
            return amount * Decimal(v[kind]) / 100
