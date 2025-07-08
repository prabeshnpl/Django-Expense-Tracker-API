from django.urls import path
from .views import register
# from .views import RegisterView, LoginView, RefreshView, ExpenseListView
urlpatterns = [
    path('auth/register',register,name='register'),
    # path('auth/login',name='login'),
    # path('auth/refresh',name='refresh'),

    # path('expenses',name='expenses'),
    
]