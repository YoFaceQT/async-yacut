import random
import string

from settings import FORBIDEN_URLS
from .models import URLMap


def generate_unique_short(length=6):
    while True:
        short = ''.join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )

        if (URLMap.query.filter_by(short=short).first() is None
                and short not in FORBIDEN_URLS):
            return short
