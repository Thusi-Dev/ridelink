from rest_framework import serializers


from .models import User, Driver, Review, Ride, CustomerReview



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ['id', 'user', 'license_number']

class RideSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    user = UserSerializer()

    class Meta:
        model = Ride
        fields = ['id', 'driver', 'user', 'pickup_location', 'dropoff_location', 'status']

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

