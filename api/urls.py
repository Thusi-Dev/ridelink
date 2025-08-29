from django.urls import path
from . import views

urlpatterns = [
    # Rides URLs
    path('rides/', views.RideListView.as_view(), name= 'ride_list'),
    path('rides/<int:pk>/', views.RideDetailView.as_view(), name= 'ride_detail'),
    path('rides/request/', views.RideRequestView.as_view(), name= 'ride_request'),

    # DriverReview URLs
    path('reviews/', views.ReviewListView.as_view(), name= 'driver_review'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name= 'driver_review_detail'),

    # CustomerReview URLs
    path('customer_reviews/', views.CustomerReviewListView.as_view()),
    path('customer_reviews/<int:pk>/', views.CustomerReviewDetailView.as_view()),
    
    # Authentication and Authorization URLs
    path('register/', views.RegisterView.as_view()),
    path('login/', views.CustomAuthTokenView.as_view()),
    
    # Parcel URLs
    path('parcels/', views.ParcelListView.as_view(), name='parcel_list'),
    path('parcels/<int:pk>/', views.ParcelDetailView.as_view(), name='parcel_detail'),
    path('parcels/request/', views.ParcelRequestView.as_view(), name='parcel_request'),
    
]