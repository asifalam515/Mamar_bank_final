from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm,TransferAmountForm,CheckWithdrawalForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from django.views import View
from .models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from .forms import ChangePasswordForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'account/user_registration.html'
    form_class = UserRegistrationForm
    success_url =reverse_lazy('register')
    def form_valid(self, form):
        # print(form.cleaned_data)
        user = form.save() #forms.py theke ouruser return kortese oita user hisebe raktesi
        login(self.request,user)
        print(user)
        return super().form_valid(form) #nijei nijeke call kore disse
    
# login log out view
class UserLoginView(LoginView):
    template_name ='account/user_login.html'
    def get_success_url(self) :
        return reverse_lazy('home')

class UserLogOutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))
    

class UserBankAccountUpdateView(View):
    template_name = 'account/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    
    
    
def transfer_amount(request):
    form = TransferAmountForm(request.POST or None)

    if form.is_valid():
        sender_username = form.cleaned_data['sender_username']
        receiver_username = form.cleaned_data['receiver_username']
        amount = form.cleaned_data['amount']

        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_username)

            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()

                messages.success(request, 'Amount transferred successfully.')
            else:
                messages.error(request, 'Insufficient funds for the transfer.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'account/transfer_amount.html', {'form': form})
    
def check_withdrawal(request):
    form = CheckWithdrawalForm(request.POST or None)

    if form.is_valid():
        user = User.objects.get(username=request.user.username)

        if user.balance > 0:
            messages.success(request, 'Withdrawal successful.')
        else:
            messages.error(request, 'The bank is bankrupt. Unable to withdraw.')

    return render(request, 'account/check_withdrawal.html', {'form': form})



# @method_decorator(login_required, name='dispatch')
# class PasswordChangeView(PasswordChangeView):
#     template_name = 'account/change_password.html'
#     success_url = reverse_lazy('register')

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form =PasswordChangeForm(user = request.user,data =request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,request.user) #password update korbe
                return redirect('profile')
        else:
            form=PasswordChangeForm(user=request.user)    
        return render(request,'account/change_password.html',{'form':form})
    else:
        return redirect('login')
            