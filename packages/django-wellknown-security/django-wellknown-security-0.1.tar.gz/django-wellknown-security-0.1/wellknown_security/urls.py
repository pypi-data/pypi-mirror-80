from django.urls import path
from .views import security_txt

urlpatterns = [
    path("security.txt", security_txt),
]