from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import Image

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

def upload_image_item(instance, filename):
    filename = instance.title + '.' + filename.split('.')[-1] #Эта конструкция задает имя файла по названию статьи
    return "{}/{}".format('image', filename)

class Item(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to=upload_image_item)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title  

class Сheckout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items_title = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.items_title  


