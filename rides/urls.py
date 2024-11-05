from django.urls import path
from . import views
from .views import RideListView, RideDetailView, BookRideView,RideCreateView
from .views import book_ride

urlpatterns = [
    path('', RideListView.as_view(), name='ride-list'),
    path('<int:id>/', RideDetailView.as_view(), name='ride-detail'),
    path('book/<int:id>/', BookRideView.as_view(), name='book_ride'),
     path('rides/<int:id>/book/', views.book_ride, name='book_ride'),
    path('rides/<int:pk>/', views.RideDetailView.as_view(), name='ride_detail'),
    path('rides/create/', RideCreateView.as_view, name='create_ride'),
    path('rides/', views.RideListView.as_view(), name='list_rides'),
]
