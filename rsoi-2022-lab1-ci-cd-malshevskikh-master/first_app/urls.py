
from django.contrib import admin
from django.urls import path

from first_app import views

urlpatterns = [
    path('api/v1/persons', views.person_list, name = 'get_post_person'),
    path('api/v1/persons/<int:pk>', views.person_just_one, name = 'get_patch_delete_person')
]
