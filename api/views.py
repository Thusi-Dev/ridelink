from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Ride, Review, CustomerReview, Parcel
from .serializers import UserSerializer, RideSerializer, ReviewSerializer, CustomerReviewSerializer, LoginSerializer, RegisterSerializer, ParcelSerializer, RideCreateSerializer, ParcelCreateSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .utils import assign_driver

# Ride views
class RideListView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

class RideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

# Parcel views
class ParcelListView(generics.ListCreateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]

class ParcelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]

# Review views
class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

# CustomerReview views
class CustomerReviewListView(generics.ListCreateAPIView):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [IsAuthenticated]

class CustomerReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
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
class CustomAuthTokenView(ObtainAuthToken):
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
        
# Ride and Parcel request views
class RideRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RideCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save(user=request.user)
        return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)

class ParcelRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParcelCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parcel = serializer.save(user=request.user)
        return Response(ParcelSerializer(parcel).data, status=status.HTTP_201_CREATED)

"""
class RideRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RideCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save(user=request.user)
        return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)

class RideListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer"""

"""
class ParcelListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

class ParcelDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
"""



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

# views.py
class RideList(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

class RideDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    
# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ride
from .serializers import RideSerializer, RideCreateSerializer
"""


"""
class RideListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

"""