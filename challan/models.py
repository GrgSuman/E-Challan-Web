from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class CustomUser(AbstractUser):
    profile = models.ImageField(default="default.png",upload_to="profile")
    date_of_birth = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=100)
    active = models.BooleanField(default=False)



class Challan(models.Model):

    VECHILE_CHOICES = (
    ("BIKE", "BIKE"),
    ("SCOOTER", "SCOOTER"),
    ("CAR", "CAR"),
    ("TRUCK", "TRUCK"),
    ("BUS", "BUS"),
    ("MINI VAN", "MINI VAN")
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    place = models.CharField(max_length=100)
    fine = models.IntegerField(default=500)
    license_number = models.IntegerField()
    vechile_number = models.IntegerField()
    vechile_type = models.CharField(choices=VECHILE_CHOICES,default="BIKE",max_length=20)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)

    def get_absolute_url(self):
        return reverse('home')