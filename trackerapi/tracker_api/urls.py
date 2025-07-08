from django.urls import path
from .views import Register, Login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/register',Register.as_view(),name='register'),
    path('auth/login',Login.as_view(),name='login'),
    path('auth/refresh',TokenRefreshView.as_view(),name='refresh'),

    # path('expenses',name='expenses'),
    
]