from django.urls import path
from .views import index


urlpatterns = [
    path('', index, name="index"),
    #path('index/', index, name="index"),
]