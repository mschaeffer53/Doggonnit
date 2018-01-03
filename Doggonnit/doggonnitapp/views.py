from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout


from .models import UserProfile, DogProfile, MissingDogReport
from django.contrib.auth.models import User, Group
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.core.mail import send_mail, EmailMultiAlternatives
from . import secret

#example of json
def test(request):
    return JsonResponse({chr(i + 96) : i for i in range(26)})

import json, requests


def get_latlng(address, city, state):
    full_address = ', '.join([address, city, state])
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    print(url)
    params = {
        'address': full_address,
        'key':secret.google_api_key
    }

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    return lat, lng


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

#log in
def mylogin(request):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('doggonnitapp:dogmap'))
    else:
        return HttpResponse('invalid credentials')

#logout
def mylogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('doggonnitapp:index'))

#create new user
def create_user_profile(request):
    name = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    points = 0

    lat, lng = get_latlng(address, city, state)

    user = User.objects.create_user(name, email, password)
    profile = UserProfile(user=user, address=address, city=city, state=state, points=points, latitude=lat, longitude=lng)
    profile.save()
    login(request, user)
    return HttpResponseRedirect(reverse('doggonnitapp:create_dog_profile'))

#add new dog to user profile
def create_dog_profile(request):
    ages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    weights = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    breeds = ['Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'Bulldog', 'Beagle',
              'Poodle', 'Rottweiler', 'Boxer', 'Pointer', 'Yorkshire Terrier', 'French Bulldog', 'Siberian Husky',
              'Great Dane', 'Doberman', 'Aussie Shepherd', 'Schnauzer', 'Corgi', 'Shih Tzu', 'Pomeranian',
              'Sheepdog', 'Snoop Dogg', 'Cocker Spaniel', 'Bernese Mountain Dog', 'Mastiff', 'Chihuahua', 'Pug', 'Maltese',
              'Newfoundland', 'Collie', 'Basset Hound', 'Akita', 'St. Bernard', 'Bloodhound', 'Whippet', 'Chow Chow',
              'Bull Terrier', 'Pit Bull', 'Greyhound', 'Aussie Cattle Dog', 'Dachshund', 'English Bulldog',
              'Jack Russel Terrier', 'Staffordshire Bull Terrier', 'Wheaton Terrier', 'Malamute']
    colors = ['Chocolate', 'Red', 'Black', 'White', 'Black and White', 'Gold or Yellow', 'Blue', 'Grey', 'Fawn', 'Cream']
    patterns = ['Single-color', 'Spotted', 'Tuxedo', 'Brindle', 'Harlequin', 'Tricolor', 'Black and Tan', 'Two-color']
    personalities = ['Aggressive', 'Playful', 'Friendly', 'Timid/shy', 'Fear-based', 'Feral', 'Rabid']
    breeds = sorted(breeds)
    colors = sorted(colors)
    patterns = sorted(patterns)
    personalities = sorted(personalities)

    context = {'weights': weights,
               'breeds': breeds,
               'colors': colors,
                'personalities': personalities,
               'patterns': patterns,
               'ages': ages}

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
        dog_description = request.POST['description']
        missing_since = None


        profile = DogProfile(name=dog_name, age=dog_age, sex=dog_sex, breed=dog_breed, color=dog_color,
                             pattern=dog_pattern, weight=dog_weight, personality=dog_personality,
                             dog_image=dog_image, description=dog_description, user=request.user, missing_since=missing_since)
        profile.save()

        return HttpResponseRedirect(reverse('doggonnitapp:dog_profile', kwargs={'dog_id':profile.id}))

    return render(request, 'doggonnitapp/addDog.html', context)



# the information for a single missing dog
def dog_profile(request, dog_id):
    dog = DogProfile.objects.get(pk=dog_id)
    profile = get_object_or_404(UserProfile, user=dog.user)
    current_user = request.user
    dog_owner = dog.user
    print(dog_owner)
    print(current_user)

    # prepare info for email
    dog_name = dog.name
    email_list = ['doggoneitapp@gmail.com']

    user_email = current_user.email
    owner_email = dog.user.email
    email_list.append(user_email)
    email_list.append(owner_email)
    print(user_email)
    print(owner_email)


    if request.method == 'POST':
        if dog_owner == current_user:  #only do this if the dog belongs to the user
            print(dog.user)
            print(current_user)
            dog.dog_is_lost = not dog.dog_is_lost
            dog.missing_since = timezone.now()
            dog.save()
            MissingDogReport.objects.filter(dog=dog).delete() #when dog is found delete missing markers
        else: #alert the dog owner with email or give the contact info
            print('notify owner')
            # send email to the owner of missing dog when someone adds a new point to the dog profile map
            send_mail(
                'Someone found ' + dog_name + '!',
                '',  # using html_message instead of plain/text
                'doggoneitapp@gmail.com',
                email_list,
                fail_silently=False,
                html_message=f'Hello {dog_owner} and {current_user}! I think we have found a match!'
                             f' {current_user} says they have found {dog_name}. Now it is up to the two of you to do the rest.'
                             f'{dog_owner}, once you get your dog back remember to update {dog_name}\'s profile to let '
                             f'everyone know they can stop looking.'

            )
    context = {'dog': dog,
               'mapbox_api_key': secret.mapbox_api_key,
               'profile': profile}


    return render(request, 'doggonnitapp/dog_profile.html', context)


# a map of all the owner reported missing dogs
def dogmap(request):
    # weights = ['less than 40 lbs', 'between 35-75 lbs', 'greater than 65 lbs']
    # colors = ['Dark', 'Light', 'Chocolate', 'Red', 'Black', 'White', 'Black and White', 'Gold or Yellow', 'Blue', 'Grey', 'Fawn', 'Cream']
    # breeds = ['Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'Bulldog', 'Beagle',
    #           'Poodle', 'Rottweiler', 'Boxer', 'Pointer', 'Yorkshire Terrier', 'French Bulldog', 'Siberian Husky',
    #           'Great Dane', 'Doberman', 'Aussie Shepherd', 'Schnauzer', 'Corgi', 'Shih Tzu', 'Pomeranian',
    #           'Sheepdog', 'Snoop Dogg', 'Cocker Spaniel', 'Bernese Mountain Dog', 'Mastiff', 'Chihuahua', 'Pug', 'Maltese',
    #           'Newfoundland', 'Collie', 'Basset Hound', 'Akita', 'St. Bernard', 'Bloodhound', 'Whippet', 'Chow Chow',
    #           'Bull Terrier', 'Pit Bull', 'Greyhound', 'Aussie Cattle Dog', 'Dachshund', 'English Bulldog',
    #           'Jack Russel Terrier', 'Staffordshire Bull Terrier', 'Wheaton Terrier', 'Malamute']
    # ages = ['puppy', 'adult', 'really old looking']

    dogs = DogProfile.objects.filter(dog_is_lost=True)
    coordinates = []
    for dog in dogs:
        profile = get_object_or_404(UserProfile, user=dog.user)
        coordinates.append({
            'lat': profile.latitude,
            'lng': profile.longitude,
            'image': dog.dog_image.url
        })
    print(coordinates)

    context = {
        # 'weights': weights,
        # 'breeds': breeds,
        # 'colors': colors,
        # 'ages': ages,
        'dogs': dogs,
        'coordinates':coordinates,
        'mapbox_api_key': secret.mapbox_api_key
    }


    return render(request, 'doggonnitapp/dogmap.html', context)


#problable wont use this
def add_marker(request):
    return HttpResponse('markers added')
    # return HttpResponseRedirect(reverse('doggonnitapp:dogmap'))

#account details
def myaccount(request):
    print(request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    dogs = DogProfile.objects.filter(user=request.user)
    return render(request, 'doggonnitapp/myaccount.html', {'profile':profile, 'dogs':dogs})

#add marker when you saw an unknown dog
def isawadog(request):
    weights = ['less than 40 lbs', 'between 35-75 lbs', 'greater than 65 lbs']
    colors = ['Dark', 'Light', 'Chocolate', 'Red', 'Black', 'White', 'Black and White', 'Gold or Yellow', 'Blue', 'Grey']
    breeds = ['Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'Bulldog', 'Beagle',
              'Poodle', 'Rottweiler', 'Boxer', 'Pointer', 'Yorkshire Terrier', 'French Bulldog', 'Siberian Husky',
              'Great Dane', 'Doberman', 'Aussie Shepherd', 'Schnauzer', 'Corgi', 'Shih Tzu', 'Pomeranian',
              'Sheepdog', 'Snoop Dogg', 'Cocker Spaniel', 'Bernese Mountain Dog', 'Mastiff', 'Chihuahua', 'Pug', 'Maltese',
              'Newfoundland', 'Collie', 'Basset Hound', 'Akita', 'St. Bernard', 'Bloodhound', 'Whippet', 'Chow Chow',
              'Bull Terrier', 'Pit Bull', 'Greyhound', 'Aussie Cattle Dog', 'Dachshund', 'English Bulldog',
              'Jack Russel Terrier', 'Staffordshire Bull Terrier', 'Wheaton Terrier', 'Malamute']
    ages = ['puppy', 'adult', 'really old looking']

    breeds = sorted(breeds)


    dogs = DogProfile.objects.filter(dog_is_lost=True)
    coordinates = []
    for dog in dogs:
        profile = get_object_or_404(UserProfile, user=dog.user)
        coordinates.append({
            'lat': profile.latitude,
            'lng': profile.longitude
        })
    print(coordinates)

    context = {
        'weights': weights,
        'breeds': breeds,
        'colors': colors,
        'ages': ages,
        'dogs': dogs,
        'coordinates':coordinates,
        'mapbox_api_key': secret.mapbox_api_key
    }

    if request.method == 'POST':
        age = request.POST['age']
        weight = request.POST['weight']
        breed = request.POST['breed']
        color = request.POST['color']
        description = request.POST['description']
        lat = request.POST['lat']
        lng = request.POST['lng']
        lat = float(lat)
        lng = float(lng)
        missing_dog_report = MissingDogReport(age=age, weight=weight, breed=breed, color=color, description=description,
                                              lat=lat, long=lng)
        missing_dog_report.save()

    return render(request, 'doggonnitapp/isawadog.html', context)

#add marker when you know which exact dog you saw
def irecognizethatdog(request, dog_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    dog = DogProfile.objects.get(pk=dog_id)

    missing_dog_report = MissingDogReport(
        dog=dog,
        age=dog.age,
        weight=dog.weight,
        breed=dog.breed,
        color=dog.color,
        description=request.POST['description'],
        lat=float(request.POST['lat']),
        long=float(request.POST['lng']),
    )
    missing_dog_report.save()

#prepare info for email
    dog_name = dog.name
    email_list = ['doggoneitapp@gmail.com']
    user_email = dog.user.email
    email_list.append(user_email)
    print(user_email)
    dog_owner = dog.user.username
    nl ='\\n' #this isnt working

    #address to dog profile
    map_address = 'http://' + request.get_host() + reverse('doggonnitapp:dog_profile', kwargs={'dog_id': dog_id})

    #send email to the owner of missing dog when someone adds a new point to the dog profile map
    send_mail(
        'Someone saw ' + dog_name + '!',
        '', #using html_message instead of plain/text
        'doggoneitapp@gmail.com',
        email_list,
        fail_silently=False,
        html_message=f'Hello {dog_owner}. Another user said they saw your dog. Go check the <a href="{map_address}">MAP</a> for the most recent location.'
                     f'{nl}Good Luck!'
    )


    return redirect('doggonnitapp:dog_profile', dog_id=dog.pk)


#map of an individual missing dog
def dogprofilemap(request, dog_id):

    dog = DogProfile.objects.get(pk=dog_id)
    dog_markers = []
    for dog_report in dog.missingdogreport_set.all():
        dog_markers.append({
            'lat':dog_report.lat,
            'lng':dog_report.long
        })
    return JsonResponse({'dog_markers':dog_markers})


#map of dogs from isawadog (unknown missing dogs)
def unknowndogmap(request):

    markers = MissingDogReport.objects.filter(dog=None)
    return render(request, 'doggonnitapp/unknowndogmap.html', {'markers':markers, 'mapbox_api_key': secret.mapbox_api_key})

