from django.urls import path
from . import views





urlpatterns = [
    path('api/consult/price', views.get_price.as_view(), name='api_consult_price'),
    path('api/consult/about', views.get_about.as_view(), name='api_consult_about'),
]