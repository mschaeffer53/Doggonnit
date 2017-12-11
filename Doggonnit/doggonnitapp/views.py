
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

from .models import BasicProfile, AdvancedProfile, DogProfile
from django.contrib.auth.models import User, Group


# Create your views here.

def index(request):
    return render(request, 'doggonnitapp/index.html', {})

def registration_page(request):
    return HttpResponse('registration page')

def mylogin(request):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('successfully logged in')
    else:
        return HttpResponse('invalid credentials')


def create_basic_profile(request):
    group = Group.objects.get(name='Basic')
    print(request.POST)
    name = request.POST['user_name']
    password = request.POST['password']
    email = request.POST['email']

    # Create user and save to the database
    user = User.objects.create_basic_profile(name, email, password)
    user.save()
    group.user_set.add(user)
    group.save()
    login(request, user)
    return HttpResponse('basic profile created and logged in')

def create_advanced_profile(request):
    group = Group.objects.get(name='Advanced')
    print(request.POST)
    name = request.POST['user_name']
    password = request.POST['password']
    email = request.POST['user_email']
    address = request.POST['user_address']
    points = request.POST['user_points']
    dogs = request.POST['user_dogs']

    user = User.objects.create_advanced_profile(name, password, email, address, points, dogs)
    user.save()
    group.user_set.add(user)
    login(request, user)
    return HttpResponse('advanced profile created and logged in')

# def create_dog_profile(request):
#     group = Group.objects.get(name='Dog')
#     print(request.POST)
#