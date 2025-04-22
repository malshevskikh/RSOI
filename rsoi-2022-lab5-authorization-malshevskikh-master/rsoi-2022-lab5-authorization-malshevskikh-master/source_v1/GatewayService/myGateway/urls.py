from django.urls import path
from . import views

urlpatterns = [
    path('flights', views.gateway_get_all_flights),
    path('tickets', views.gateway_get_all_tickets_and_buy),
    path('tickets/<uuid:ticketUid>', views.gateway_get_ticket_info_and_cancel),
    path('me', views.gateway_get_user_info),
    path('privilege', views.gateway_get_privilege_info)
]