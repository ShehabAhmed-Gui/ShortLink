import string
import random
from ..models import Urls
from django.core.cache import cache 

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
BASE = len(ALPHABET)

def cache_response(key, value, timeout=15*60):
    cache.set(key, value, timeout=timeout)


def get_cache(key):
    return cache.get(key)


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits

    while True:
        short_url = ''.join(random.choices(chars, k=length))

        if not Urls.objects.filter(short_url=short_url).exists():
            return short_url