from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class DogProfile(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    sex = models.CharField(max_length=6)
    breed = models.CharField(max_length=50)
    color = models.CharField(max_length=25)
    pattern = models.CharField(max_length=25)
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(250)])
    personality = models.CharField(max_length=25)
    dog_is_lost = models.BooleanField(default=False)
    dog_image = models.ImageField()
    description = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    missing_since = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'{self.name} {self.age} {self.sex} {self.breed} {self.pattern}' \
               f'{self.color} {self.weight} {self.personality} {self.description} {self.dog_is_lost}'


class UserProfile(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    points = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.user.username} {self.address} {self.city} {self.state} {self.points}'


class MissingDogReport(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    lat = models.FloatField()
    long = models.FloatField()
    description = models.TextField(default='')
    weight = models.CharField(max_length=25)
    age = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    breed = models.CharField(max_length=50)
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        if self.dog:
            return f'{self.dog.name} {self.timestamp} {self.description} {self.weight} {self.age} {self.color} {self.breed}'
        else:
            return f'{self.timestamp} {self.description} {self.weight} {self.age} {self.color} {self.breed}'



