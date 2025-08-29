from django.urls import path
from . import views

urlpatterns = [
    # Ride URLs
    path('rides/', views.RideList.as_view()),
    path('rides/<int:pk>/', views.RideDetail.as_view()),

    # Review URLs
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()),

    # CustomerReview URLs
    path('customer-reviews/', views.CustomerReviewList.as_view()),
    path('customer-reviews/<int:pk>/', views.CustomerReviewDetail.as_view()),
    
    # Authentication and Authorization URLs
    path('register/', views.RegisterView.as_view()),
    path('login/', views.CustomAuthToken.as_view()),
    
    # Ride Booking URL
    path('ride/',views.RideBookingView.as_view()),
]