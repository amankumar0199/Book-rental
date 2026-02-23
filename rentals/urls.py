from django.urls import path
from .views import CreateRentalView, RentalListView, ExtendRentalView

urlpatterns = [
    path("rent/", CreateRentalView.as_view()),
    path("rentals/", RentalListView.as_view(), name="rental-list"),
    path("rentals/<int:rental_id>/extend/", ExtendRentalView.as_view(), name="extend-rental")
]
