from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('categories/', categories, name='categories'),
    path('blog/', blog_detail, name='blog_detail'),
]
