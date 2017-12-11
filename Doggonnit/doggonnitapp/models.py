from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class DogProfile(models.Model):
    dog_name = models.CharField(max_length=25)
    dog_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    dog_sex = models.CharField(max_length=6)
    dog_breed = models.CharField(max_length=50)
    dog_color = models.CharField(max_length=20)
    dog_weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MinValueValidator(250)])
    dog_personality = models.CharField(max_length=25)
    dog_is_lost = models.BooleanField(default=False)
    dog_image = models.ImageField(upload_to='pic_folder/')
    #dog_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dog_name} {self.dog_age} {self.dog_sex} {self.dog_breed}' \
               f'{self.dog_color} {self.dog_weight} {self.dog_personality} {self.dog_is_lost}'


class AdvancedProfile(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_address = models.CharField(max_length=75)
    user_points = models.PositiveIntegerField()
    user_dogs = models.ForeignKey(DogProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_name} {self.user_email} {self.user_address} {self.user_points} {self.user_dogs}'

class BasicProfile(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_points = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user_name} {self.user_email} {self.user_points}'