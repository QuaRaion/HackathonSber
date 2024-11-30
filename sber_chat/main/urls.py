from django.contrib import admin
from django.urls import include, path
from main import views

urlpatterns = [
    path('', views.render_main_page, name='main'),
]
