from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', BlogListView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', search, name='search'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    # path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<slug:slug>/', blog_detail, name='blog-detail'),
    path('category/', category, name='category'),
    path('category/<slug:slug>/', CategoryView, name='category-view'),
    

    # path('send_comment/<slug:slug>/', send_comment, name='send_comment'),
]
