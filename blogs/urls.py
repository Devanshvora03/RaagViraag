from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', contact, name='contact'),
    
]
