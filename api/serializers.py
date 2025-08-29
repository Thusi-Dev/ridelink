from rest_framework import serializers
from .models import User, Driver, Review, Ride, CustomerReview, Parcel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'username', 'email']
        
class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ['id', 'user', 'license_number']
        
# Ride Serializer
class RideSerializer(serializers.ModelSerializer):
    pickup_location = serializers.ReadOnlyField(source='pickup_location')
    dropoff_location = serializers.ReadOnlyField(source='dropoff_location')
    driver = DriverSerializer()
    user = UserSerializer()

    class Meta:
        model = Ride
        fields = ['id', 'driver', 'user', 'pickup_location', 'dropoff_location', 'ride_type', 'status']

# RideCreate serializer
class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'ride_type']
        
# Parcel serializer
class ParcelSerializer(serializers.ModelSerializer):
    ride = RideSerializer()
    user = UserSerializer()

    class Meta:
        model = Parcel
        fields = '__all__'
        
# ParcelCreate serializer
class ParcelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ['ride', 'parcel_type', 'parcel_weight', 'parcel_dimensions']
        
class ReviewSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    user = UserSerializer()

    class Meta:
        model = Review
        fields = ['id', 'driver', 'user', 'rating', 'review', 'created_at']

class CustomerReviewSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    customer = UserSerializer()
    ride = RideSerializer()

    class Meta:
        model = CustomerReview


        fields = ['id', 'driver', 'customer', 'ride', 'rating', 'review', 'created_at']

"""
class ParcelSerializer(serializers.ModelSerializer):
    pickup_location = serializers.ReadOnlyField(source='pickup_location')
    dropoff_location = serializers.ReadOnlyField(source='dropoff_location')

    class Meta:
        model = Parcel
        fields = ['id', 'ride', 'parcel_type', 'parcel_description', 'parcel_weight', 'parcel_dimensions', 'status', 'pickup_location', 'dropoff_location']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid credentials')
"""

from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['identifier'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid credentials')

from django.db import IntegrityError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError('Username or email already exists')