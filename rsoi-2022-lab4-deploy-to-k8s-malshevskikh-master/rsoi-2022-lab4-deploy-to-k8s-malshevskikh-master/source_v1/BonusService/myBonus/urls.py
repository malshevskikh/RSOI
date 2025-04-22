from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/privilege', views.get_userinfo_about_bonus),
    path('api/v1/privilege_history', views.get_userinfo_about_history),
    path('api/v1/change_count', views.change_privilege_count),
    path('api/v1/return_money/<uuid:ticket_id>', views.return_privilege_count)
]