from django.urls import path
from . import views

from django.urls import path
from .views import RideListView, RideDetailView, BookRideView

urlpatterns = [
    path('', RideListView.as_view(), name='ride-list'),
    path('<int:id>/', RideDetailView.as_view(), name='ride-detail'),
    path('book/<int:id>/', BookRideView.as_view(), name='ride-book'),
    path('ride/<int:pk>/', views.RideDetailView.as_view(), name='ride_detail'),
    path('rides/', views.RideListView.as_view(), name='list_rides'),
]
