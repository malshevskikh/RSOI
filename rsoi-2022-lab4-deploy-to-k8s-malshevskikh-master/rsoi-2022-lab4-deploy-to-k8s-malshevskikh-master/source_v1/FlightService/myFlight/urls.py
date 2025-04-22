from django.urls import path
from . import views

urlpatterns = {
    path('api/v1/flights/<str:flight_num>', views.get_one_flight),
    path('api/v1/flights', views.get_list_of_flights)
}
