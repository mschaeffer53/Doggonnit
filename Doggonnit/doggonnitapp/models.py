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

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.age} {self.sex} {self.breed} {self.pattern}' \
               f'{self.color} {self.weight} {self.personality} {self.dog_is_lost}'


class UserProfile(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    points = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} {self.address} {self.city} {self.state} {self.points}'