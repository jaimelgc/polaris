import random
import string


def random_alphanum(pin_lenght):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=pin_lenght))
