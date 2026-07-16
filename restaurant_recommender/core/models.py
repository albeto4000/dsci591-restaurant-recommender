from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid

class Restaurant(models.Model):
  id = models.CharField(max_length = 22, primary_key = True)
  name = models.CharField(max_length = 100)
  address = models.CharField(max_length = 200)
  city = models.CharField(max_length = 100)
  state = models.CharField(max_length = 3)
  postal_code = models.CharField(max_length = 10)
  latitude = models.FloatField()
  longitude = models.FloatField()
  stars = models.FloatField()
  review_count = models.IntegerField()
  is_open = models.BooleanField(default = True)
  attributes = models.TextField()
  categories = models.TextField()
  hours = models.TextField()

  def __str__(self):
    return self.name

  def first_review(self):
      # Excludes empty strings and None values
      return self.review_set.exclude(rating__lt=4).exclude(review__exact='').exclude(review__isnull=True).first()

class CustomUser(AbstractUser):
  id = models.CharField(max_length = 22, primary_key = True, editable = False)

class Review(models.Model):
  id = models.CharField(max_length = 22, primary_key = True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
  business = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
  rating = models.IntegerField()
  useful = models.IntegerField()
  funny = models.IntegerField()
  cool = models.IntegerField()
  review = models.TextField()
  date = models.DateField(default = timezone.now)

  def __str__(self):
    return self.review