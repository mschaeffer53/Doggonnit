
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

from .models import UserProfile, DogProfile
from django.contrib.auth.models import User, Group


# Create your views here.

def index(request):
    return render(request, 'doggonnitapp/index.html', {})

def registrationPage(request):
    return render(request, 'doggonnitapp/registrationPage.html', {})

def mylogin(request):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('successfully logged in')
    else:
        return HttpResponse('invalid credentials')


def create_user_profile(request):
    print(request.POST)
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

# def create_dog_profile(request):