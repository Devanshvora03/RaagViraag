from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
]
