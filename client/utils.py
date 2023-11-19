import random
import string


# returns a randomly generated string of decimal digits and uppercase letters
def random_alphanum(lenght: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=lenght))
