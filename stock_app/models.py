from datetime import datetime
from email.policy import default
from enum import unique
from unicodedata import name
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    full_name = models.CharField(max_length=70)
    # username = models.CharField(max_length=50)
    phone = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=62)
    status = models.BooleanField(default=True)
    email = models.CharField(max_length=25)

class Role(models.Model):
    name = models.CharField(max_length=25)
    status = models.BooleanField(default=True)

class User_role(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    role = models.ForeignKey(Role,on_delete=CASCADE)

class Permission(models.Model):
    name = models.CharField(max_length=25)
    status = models.BooleanField(default=True)
    slug = models.CharField(max_length=25)

class Role_permission(models.Model):
    role = models.ForeignKey(Role,on_delete=CASCADE)
    permission = models.ForeignKey(Permission,on_delete=CASCADE)

class Images(models.Model):
    title = models.CharField(max_length=35)
    url = models.ImageField(blank=True,null=True,upload_to="images/")
    status = models.BooleanField(default=True)
    location = models.CharField(max_length=35,null=True,blank=True)
    description = models.TextField()
    user = models.ForeignKey(User,on_delete=CASCADE)
    liked = models.ManyToManyField(User,through='Like',related_name="liked",blank=True,default=None)
    like_count = models.BigIntegerField(default='0')
    
    def __str__(self):
        return self.title

class Like(models.Model):
    image = models.ForeignKey(Images,on_delete=CASCADE)
    user = models.ForeignKey(User,on_delete=CASCADE)
    timestamp = datetime.now()

    class Meta:
        unique_together= [['image', 'user' ]]

class Categories(models.Model):
    name = models.CharField(max_length=25,unique=True)
    slug = models.CharField(max_length=25,unique=True)
    parent = models.ForeignKey("self",on_delete=CASCADE,default=None,blank=True,null=True)
    images = models.ManyToManyField(Images,through='Image_category',related_name='image_categories',blank=True,default=None)

    def __str__(self):
        return self.name

class Image_category(models.Model):
    images = models.ForeignKey(Images,on_delete=CASCADE)
    category = models.ForeignKey(Categories,on_delete=CASCADE)



