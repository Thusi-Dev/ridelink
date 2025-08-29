from django.contrib import admin


# Register your models here




from .models import Driver, Ride, User, Parcel



admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Ride)
admin.site.register(Parcel)