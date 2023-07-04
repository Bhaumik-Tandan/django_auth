from django.contrib import admin
from django.urls import path, include
from user.views import signup, login_view, get_users, calculate_incentive

urlpatterns = [
    path('api/signup', signup, name='signup'),
    path('api/login', login_view, name='login'),
    path('', get_users, name='get_users'),
    path('api/incentive/<int:user_id>/', calculate_incentive, name='calculate_incentive'),

    # Add other app URLs if needed
]
