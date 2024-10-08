import random
import string

from .models import URLMap


def get_unique_short_id():
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choices(characters, k=6))
    while URLMap.query.filter_by(short=short_id).first():
        short_id = ''.join(random.choices(characters, k=6))
    return short_id