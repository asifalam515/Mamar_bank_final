
from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserLogOutView,UserBankAccountUpdateView,user_logout
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    # path('logout/', UserLogOutView.as_view(),name='logout'),
    path('logout/', user_logout,name='logout'),
    path('profile/', UserBankAccountUpdateView.as_view(), name='profile' )
    
]