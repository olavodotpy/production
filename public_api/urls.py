from django.urls import path
from . import views





urlpatterns = [
    path('api-private/consult/price', views.get_data_endpoint_public.as_view(), name='private')
]