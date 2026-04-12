from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils.url_utils import generate_short_url, cache_response, get_cache

from django.utils import timezone
from datetime import timedelta

from ..models import Urls

class UrlAPIView(APIView):
    def validate_url(self, url):
        if url is None:
            return Response({
                'type': 'error',
                'message': 'invalid url'
            }, status=400)
        
    def generate_cache_key(self, short_url):
        key = f'long_url:short_url:{short_url}'
        return key
    
    # Retrieves original url via short_url
    def get(self, request, short_url):
        key = self.generate_cache_key(short_url)
        resposne = get_cache(key)
        if resposne is not None:
            print('Cache Hit')
            return Response(resposne)

        print('Cache Miss')
        url = get_object_or_404(Urls, short_url=short_url)
        response = {
            'short_url': short_url,
            'original_url': url.long_url,
            'created_at': url.created_at,
            'deactivate_date': url.deactivate_date
        }

        cache_response(key, response, timeout=15*60)
        return Response(response)
        
    def post(self, request):
        long_url = request.data.get('url')
        self.validate_url(long_url)

        short_url = generate_short_url(long_url)
        created_at = timezone.now()
        deactivate_at = created_at + timedelta(days=30)

        record = Urls(long_url=long_url, short_url=short_url.split('/'),
                    created_at=created_at,
                    deactivate_date=deactivate_at
                    )
        record.save()
        return Response({
            'url': long_url,
            'short_url': short_url,
            'created_at': created_at,
            'deactivate_at': deactivate_at
        })
    
    def put(self, request, short_url):
        # Update short url
        long_url = request.data.get('url')
        self.validate_url(long_url)
        
        record = get_object_or_404(Urls, short_url=short_url)
        record.long_url = long_url
        record.save()

        response = {
            'url': long_url,
            'short_url': short_url,
            'created_at': record.created_at,
            'deactivate_date': record.deactivate_date
        }

        key = self.generate_cache_key(short_url)
        cache_response(key, response)
        return Response(response)
