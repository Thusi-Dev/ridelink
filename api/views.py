from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Ride, Review, CustomerReview
from .serializers import UserSerializer, RideSerializer, ReviewSerializer, CustomerReviewSerializer, LoginSerializer, RegisterSerializer, ParcelSerializer, RideCreateSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .utils import assign_driver

# Ride views
class RideList(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

class RideDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

# Review views
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

# CustomerReview views
class CustomerReviewList(generics.ListCreateAPIView):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [IsAuthenticated]

class CustomerReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [IsAuthenticated]
    
# User Registration view  
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# User login view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name': user.get_full_name() or user.username,
        })
"""
# Ride Booking view       
class RideBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save(user=request.user)
            # Assign a driver to the ride
            driver = assign_driver(ride)
            if driver:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No drivers available'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class RideBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RideCreateSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save(user=request.user)
            driver = assign_driver(ride)
            if driver:
                ride_serializer = RideSerializer(ride)
                return Response(ride_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No drivers available'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
