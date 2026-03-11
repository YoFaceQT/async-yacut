import random
import string

from .models import URLMap
from settings import FORBIDEN_URLS


def generate_unique_short(length=6):
    short = ''.join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
    while URLMap.query.filter_by(short=short).first() is not None:
        short = generate_unique_short()
    while short in FORBIDEN_URLS:
        short = generate_unique_short()
    return short
