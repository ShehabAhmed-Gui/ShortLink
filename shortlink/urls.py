from django.urls import path
from .views.api_views import UrlAPIView
from .views.redirect_views import RedirectView

urlpatterns = [
    path('shortlink/', UrlAPIView.as_view()),
    path('shortlink/<str:short_url>/', UrlAPIView.as_view()),
    path('shortlink/<str:short_url>', RedirectView.as_view()),
]