from .views import *
from django.urls import path

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    # path('categories/', categories, name='categories'),
    # path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<slug:slug>/', blog_detail, name='blog-detail'),
    path('category/<slug:slug>/', CategoryView, name='category-detail'),
]
