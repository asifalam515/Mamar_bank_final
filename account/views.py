from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse,reverse_lazy
from django.views import View

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
    
    