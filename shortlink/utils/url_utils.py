import hashlib
from ..models import Urls
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache 

def cache_response(key, value, timeout=15*60):
    cache.set(key, value, timeout=timeout)

def get_cache(key):
    return cache.get(key)

def generate_short_url(long_url):
    """

    First, checks if hashed value is in the db
    if yes, calculates the id for this new record and appends it

    """

    hash = hashlib.md5(long_url.encode())
    short_url = hash.hexdigest()[:5]

    try:
        Urls.objects.get(short_url=short_url)
    except ObjectDoesNotExist:
        return short_url

    last_id = Urls.objects.order_by('-id').values_list('id', flat=True).first()
    short_url += str(last_id)

    return short_url
