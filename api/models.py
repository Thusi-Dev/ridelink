from django.db import models

# Create your models here
    
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]
    DRIVER_STATUS = [
    	('pending', 'Pending'),
    	('approved', 'Approved'),
    	('rejected', 'Rejected'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='customer')
    driver_status = models.CharField(max_length=10, choices=DRIVER_STATUS, default='not_applied')
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    vehicle_type = models.CharField(max_length=100)
    vehicle_make = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_vin = models.CharField(max_length=17, unique=True)
    vehicle_registration_number = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50)
    license_expiry_date = models.DateField()
    insurance_provider = models.CharField(max_length=100)
    insurance_policy_number = models.CharField(max_length=50)
    insurance_expiry_date = models.DateField()
    availability = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    location_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    location_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    location = models.CharField(max_length=255, default='Current Location')
    
    def save(self, *args, **kwargs):
        self.location = f"{self.location_latitude}, {self.location_longitude}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_type}"
        
"""
class Ride(models.Model):
    RIDE_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('shared', 'Shared'),
        ('luxury', 'Luxury'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True, related_name='rides')
    pickup_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    pickup_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    dropoff_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    dropoff_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    pickup_location = models.CharField(max_length=255, default='Current Location')
    destination = models.CharField(max_length=255)
    ride_type = models.CharField(max_length=100, choices=RIDE_TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='requested')
    
    def save(self, *args, **kwargs):
        self.pickup_location = f"{self.pickup_latitude}, {self.pickup_longitude}"
        self.destination = f"{self.dropoff_latitude}, {self.dropoff_longitude}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ride {self.id} - {self.user.username}"
"""        

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.driver.user.username} by {self.user.username}"
       
class CustomerReview(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='customer_reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_reviews')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='customer_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.customer.username} by {self.driver.user.username}"

"""      
class Parcel(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    parcel_type = models.CharField(max_length=255)
    parcel_description = models.TextField()
    parcel_weight = models.DecimalField(max_digits=5, decimal_places=2)
    parcel_dimensions = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    @property
    def pickup_location(self):
        return self.ride.pickup_location

    @property
    def dropoff_location(self):
        return self.ride.destination
"""

# Request model
class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    pickup_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    dropoff_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    dropoff_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    class Meta:
        abstract = True

# Ride model inheriting Request model
class Ride(Request):
    RIDE_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('shared', 'Shared'),
        ('luxury', 'Luxury'),
    ]

    ride_type = models.CharField(max_length=100, choices=RIDE_TYPE_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def pickup_location(self):
        return f"{self.pickup_latitude}, {self.pickup_longitude}"

    @property
    def dropoff_location(self):
        return f"{self.dropoff_latitude}, {self.dropoff_longitude}"
        
# Parcel model inheriting Request model
class Parcel(Request):
    PARCEL_TYPE_CHOICES = [
        ('documents', 'Documents'),
        ('packages', 'Packages'),
    ]

    parcel_type = models.CharField(max_length=100, choices=PARCEL_TYPE_CHOICES)
    parcel_weight = models.DecimalField(max_digits=5, decimal_places=2)
    parcel_dimensions = models.CharField(max_length=255)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True, blank=True)