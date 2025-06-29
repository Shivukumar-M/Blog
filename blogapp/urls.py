from django.contrib import admin
from django.urls import path
from blogapp import views

urlpatterns = [
    # path('helo/',views.helo, name='helo')
    path('<slug:slug>/', views.detail, name='detail' ),
    path('',views.index, name='index')
]
