from .models import Driver, Ride
from geopy.distance import geodesic

def assign_driver(ride):
    # Get all available drivers
    available_drivers = Driver.objects.filter(availability='available')

    # Calculate the distance between each driver and the ride's pickup location
    closest_driver = None
    closest_distance = float('inf')
    for driver in available_drivers:
        driver_location = (driver.location_latitude, driver.location_longitude)
        ride_pickup_location = (ride.pickup_latitude, ride.pickup_longitude)
        distance = geodesic(driver_location, ride_pickup_location).miles
        if distance < closest_distance and distance <= 10:  # 10-mile threshold
            closest_driver = driver
            closest_distance = distance

    # Assign the closest driver to the ride
    if closest_driver:
        closest_driver.availability = 'busy'
        closest_driver.save()
        ride.driver = closest_driver
        ride.save()
        return closest_driver
    else:
        return None