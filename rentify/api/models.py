from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# Create your models here.

# model for Users
class User(AbstractUser):
    avatar = models.CharField(max_length=150, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    phoneNumber = models.CharField(max_length=15)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username

#model for house Listing
class Listing(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    address = models.TextField()
    regularPrice = models.DecimalField(max_digits=10, decimal_places=2)
    discountPrice = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    bathrooms = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    furnished = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    type = models.CharField(max_length=50)
    offer = models.BooleanField(default=False)
    imageUrls = models.TextField()
    userRef = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

   
    def get_imageUrls(self):

        return json.loads(self.imageUrls)
    
    def __str__(self):

        return self.name






    

