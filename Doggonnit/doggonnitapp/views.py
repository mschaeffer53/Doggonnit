
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
        return HttpResponse('successfully logged in')
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
    breeds = ['lab', 'poodle', 'labradoodle']
    colors = ['chocolate', 'red', 'spotted', 'tuxedo', 'black', 'white', 'black and white', 'gold or yellow', 'blue', 'grey', 'fawn', 'cream']
    personalities = ['aggressive', 'playful', 'friendly', 'timid/shy', 'feral', 'rabid']

    if request.method == 'POST':
        dog_name = request.POST['dog_name']
        dog_age = request.POST['dog_age']
        dog_sex = request.POST['dog_sex']
        dog_breed = request.POST['dog_breed']
        dog_color = request.POST['dog_color']
        dog_weight = request.POST['dog_weight']
        dog_personality = request.POST['dog_personality']
        dog_image = request.FILES['dog_image']

        profile = DogProfile(dog_name=dog_name, dog_age=dog_age, dog_sex=dog_sex, dog_breed=dog_breed, dog_color=dog_color,
                            dog_weight=dog_weight, dog_personality=dog_personality, dog_image=dog_image, user=request.user)
        profile.save()

        return HttpResponseRedirect(reverse('doggonnitapp:dog_profile', kwargs={'dog_id':profile.id}))

    return render(request, 'doggonnitapp/addDog.html', {'weights': weights, 'breeds': breeds, 'colors': colors, 'personalities': personalities})

def success(request):
    return HttpResponse('success')

def dog_profile(request, dog_id):
    dog = DogProfile.objects.get(pk=dog_id)
    return render(request, 'doggonnitapp/dog_profile.html', {'dog':dog})

# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['dog_image']:
#         myfile = request.FILES['dog_image']
#         fs = FileSystemStorage()
#         filename = fs.save(dog_image.name, dog_image)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'core/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'core/simple_upload.html')