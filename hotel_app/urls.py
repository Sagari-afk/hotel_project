from django.urls import path

from hotel_app.views import (
    api_hotels,
    api_booking,
    api_cities,
)

urlpatterns = [
    path("hotels/", api_hotels),
    path("booking/", api_booking),
    path("cities/", api_cities)
]
