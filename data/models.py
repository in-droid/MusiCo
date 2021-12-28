from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

# Create your models here.


# You can change the DEFAULT values to anything you want...

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255, null=False)
    country = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.city+', '+self.country


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    info = models.CharField(max_length=255, null=True, default="No info!")
    img_link = models.CharField(max_length=1000, null=True, default="No image link!")

    def __str__(self):
        return self.name


class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    info = models.CharField(max_length=255, null=True, default="No info!")
    additional_info = models.CharField(max_length=500, null=True, default="No additional info!")
    img_link = models.CharField(max_length=1000, null=True, default="No image link!")

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    vid = models.ForeignKey(Venue, on_delete=models.CASCADE)
    aid = models.ForeignKey(Artist, on_delete=models.CASCADE)
    lid = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField(null=True, default="No date yet!")
    lineup = models.CharField(max_length=500, null=True, default="No lineup!")
    additional_info = models.CharField(max_length=1000, null=True, default="No additional info!")
    tickets = models.CharField(max_length=1000, null=True, default="No tickets yet!")

    def __str__(self):
        return str(self.aid)+' -- '+str(self.vid)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Artist_Genre(models.Model):
    id = models.AutoField(primary_key=True)
    aid = models.ForeignKey(Artist, on_delete=models.CASCADE)
    gid = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.aid)+' -- '+str(self.gid)

