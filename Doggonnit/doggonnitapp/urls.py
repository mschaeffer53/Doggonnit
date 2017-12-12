from django.conf.urls import url
from . import views


app_name = 'doggonnitapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mylogin/$', views.mylogin, name='mylogin'),
    url(r'^registration/$', views.registrationPage, name='registrationPage'),
    url(r'^create_user_profile/$', views.create_user_profile, name='create_user_profile')
]
