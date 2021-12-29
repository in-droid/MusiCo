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



# Uncomment down below

# # Add items to list for more locations...
countries = ['Slovenia']
cities = ['Ljubljana']


#if database is empty:
if len(Artist.objects.all()) == 0:
     for city, country in zip(cities, countries):
         init.InitDatabase(city, country)