from django.urls import path

from core.views import PhoneView


urlpatterns = [
    path("", PhoneView.as_view(), name="phone"),
]
