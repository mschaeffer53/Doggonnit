from django.conf.urls import url
from . import views


app_name = 'doggonnitapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mylogin/$', views.mylogin, name='mylogin'),
    url(r'^registration/$', views.registration_page, name='registration_page'),

]
