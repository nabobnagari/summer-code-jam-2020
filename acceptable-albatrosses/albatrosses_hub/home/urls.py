from django.urls import path, include
from .views import homepage, about_us

urlpatterns = [
    path("", homepage, name="homepage"),
    path("about_us", about_us, name="about_us"),
]
