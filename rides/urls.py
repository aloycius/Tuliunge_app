from django.urls import path
from . import views

from django.urls import path
from .views import RideListView, RideDetailView, BookRideView

urlpatterns = [
    path('', RideListView.as_view(), name='ride-list'),
    path('<int:id>/', RideDetailView.as_view(), name='ride-detail'),
    path('<int:id>/book/', BookRideView.as_view(), name='ride-book'),
]
