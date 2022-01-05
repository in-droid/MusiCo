from django.contrib import admin

# Register your models here.

from .models import *

from .DataBase import init

admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Genre)
admin.site.register(Artist_Genre)
admin.site.register(Location)
admin.site.register(User_Genre)
admin.site.register(SpotifyToken)
admin.site.register(User_Artist)



# Uncomment down below

# # Add items to list for more locations...
countries = ['Slovenia']
cities = ['Ljubljana']


# for city, country in zip(cities, countries):
#     #if database is empty:
#     if len(Location.objects.filter(country=country).filter(city=city)) == 0:
#         init.InitDatabase(city, country)