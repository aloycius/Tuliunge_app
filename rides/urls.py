from django.urls import path
from . import views
from .views import RideCreateView, RideListView, RideDetailView, RideBookingView

urlpatterns = [
    path('rides', RideCreateView.as_view(), name='ride-create'),
    path('rides', RideListView.as_view(), name='ride-list'),
    path('rides/<int:id>', RideDetailView.as_view(), name='ride-detail'),
    path('rides/<int:id>/book', RideBookingView.as_view(), name='ride-book'),
]
