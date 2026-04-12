from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseNotFound
from ..utils.url_utils import cache_response, get_cache
from rest_framework.views import APIView

from ..models import Urls

class RedirectView(APIView):
    def generate_redirect_cache_key(self, short_url):
        key = f'redirect:short_url:{short_url}'
        return key
    # Get long_url via short_url and redirect user
    def get(self, request, short_url):
        if short_url is None:
            return HttpResponseNotFound('invalid short_url')
        
        key = self.generate_redirect_cache_key(short_url)
        redirect_url = get_cache(key)
        if redirect_url is None:
            print('Cache Miss')
            record = get_object_or_404(Urls, short_url=short_url)
            long_url = record.long_url

            cache_response(key, long_url)
            return redirect(long_url)

        print('Cache Hit')
        return redirect(redirect_url)
