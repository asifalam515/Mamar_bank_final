
from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserLogOutView,UserBankAccountUpdateView,user_logout,transfer_amount,check_withdrawal,change_password
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    # path('logout/', UserLogOutView.as_view(),name='logout'),
    path('logout/', user_logout,name='logout'),
    path('profile/', UserBankAccountUpdateView.as_view(), name='profile' ),
    path('transfer_amount/', transfer_amount, name='transfer_amount'),
    path('check_withdrawal/', check_withdrawal, name='check_withdrawal'),
    path('change_password/', change_password,name='change_password'),
    
]