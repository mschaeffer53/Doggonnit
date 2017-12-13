
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

from .models import UserProfile, DogProfile
from django.contrib.auth.models import User, Group
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'doggonnitapp/index.html', {})

def registrationPage(request):
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return render(request, 'doggonnitapp/registrationPage.html', {'states': states})

def mylogin(request):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('doggonnitapp:dogmap'))
    else:
        return HttpResponse('invalid credentials')


def create_user_profile(request):
    name = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    points = 0

    user = User.objects.create_user(name, email, password)
    profile = UserProfile(user=user, address=address, city=city, state=state, points=points)
    profile.save()
    login(request, user)
    return HttpResponse('new profile created and logged in')

def create_dog_profile(request):
    weights = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    breeds = ['Lab', 'Poodle', 'Labradoodle', 'Mutt']
    colors = ['Chocolate', 'Red', 'Black', 'White', 'Black and White', 'Gold or Yellow', 'Blue', 'Grey', 'Fawn', 'Cream']
    patterns = ['Spotted', 'Tuxedo', 'Brindle', 'Harlequin', 'Tricolor', 'Black and Tan']
    personalities = ['Aggressive', 'Playful', 'Friendly', 'Timid/shy', 'Feral', 'Rabid']

    if request.method == 'POST':
        dog_name = request.POST['name']
        dog_age = request.POST['age']
        dog_sex = request.POST['sex']
        dog_breed = request.POST['breed']
        dog_color = request.POST['color']
        dog_pattern = request.POST['pattern']
        dog_weight = request.POST['weight']
        dog_personality = request.POST['personality']
        dog_image = request.FILES['dog_image']

        profile = DogProfile(name=dog_name, age=dog_age, sex=dog_sex, breed=dog_breed, color=dog_color, pattern=dog_pattern,
                             weight=dog_weight, personality=dog_personality, dog_image=dog_image, user=request.user)
        profile.save()

        return HttpResponseRedirect(reverse('doggonnitapp:dog_profile', kwargs={'dog_id':profile.id}))

    return render(request, 'doggonnitapp/addDog.html', {'weights': weights, 'breeds': breeds, 'colors': colors,
                                                        'personalities': personalities, 'patterns':patterns})


def success(request):
    return HttpResponse('success')

def dog_profile(request, dog_id):
    dog = DogProfile.objects.get(pk=dog_id)
    if request.method == 'POST':
        dog.dog_is_lost = not dog.dog_is_lost
        dog.save()
    return render(request, 'doggonnitapp/dog_profile.html', {'dog':dog})

def dogmap(request):
    return render(request, 'doggonnitapp/dogmap.html', {})

