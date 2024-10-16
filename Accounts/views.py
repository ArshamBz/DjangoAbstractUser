from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# User Registration View (CreateView)
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'Accounts/register.html'
    success_url = reverse_lazy('home')  # Redirect to 'home' after successful registration

    def form_valid(self, form):
        # Save the form and log in the user
        response = super().form_valid(form)
        phone_number = form.cleaned_data.get('phone_number')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(phone_number=phone_number, password=raw_password)
        if user is not None:
            login(self.request, user)
        return response


# User Login View (FormView)
class UserLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'Accounts/login.html'
    success_url = reverse_lazy('home')  # Redirect to 'home' after successful login

    def form_valid(self, form):
        phone_number = form.cleaned_data.get('username')  # Get phone_number as username
        password = form.cleaned_data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
