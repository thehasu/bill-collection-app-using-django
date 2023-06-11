from datetime import datetime

import django
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

# Create your models here.
User = get_user_model()


class Month(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=50)
    numberofchannels = models.IntegerField(default=0)
    numberofHDchannels = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.name + "  ($" + str(self.price) + ")"


class Collection(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    billDate = models.DateField(auto_now_add=False,  blank=True, default=datetime.now)
    billMonth = models.ForeignKey(
        Month, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return str(self.billMonth)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    fullname = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(
        upload_to='bill_coll_images', default='placeholderimg.jpg')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100)
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, blank=True, null=True)
    paidThruMonth = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.fullname
