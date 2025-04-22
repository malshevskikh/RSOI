from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/tickets', views.get_all_tickets_of_user),
    path('api/v1/tickets/<uuid:ticketUid>', views.get_one_tickets_of_user),
    path('api/v1/tick', views.buy_ticket_for_user),
    path('api/v1/del_tick/<uuid:ticketUid>', views.delete_ticket)
]