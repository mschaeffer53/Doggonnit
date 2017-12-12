from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'doggonnitapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mylogin/$', views.mylogin, name='mylogin'),
    url(r'^registration/$', views.registrationPage, name='registrationPage'),
    url(r'^create_user_profile/$', views.create_user_profile, name='create_user_profile'),
    url(r'^create_dog_profile/$', views.create_dog_profile, name='create_dog_profile'),
    url(r'dog_profile/(?P<dog_id>[0-9]+)/', views.dog_profile, name='dog_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)