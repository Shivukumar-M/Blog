from django.contrib import admin
from django.urls import path
from blogapp import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('archive/', views.archive, name='archive'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.detail, name='detail'),
]
