from django.shortcuts import render
from django.views.generic import CreateView,DetailView
from .forms import SignUpForm,RegistProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404

# Create your views here.
class SignUp(CreateView):
    form_class=SignUpForm
    template_name='account/signup.html'
    success_url=reverse_lazy('account:registprofile')

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        self.object=user
        return HttpResponseRedirect(self.get_success_url())
        

class RegistProfileView(CreateView):
    form_class=RegistProfileForm
    template_name='account/registprofile.html'
    success_url=reverse_lazy('top')

    def form_valid(self, form):
        profile=form.save(commit=False)
        profile.user=self.request.user
        profile.save()
        self.object=profile
        return HttpResponseRedirect(self.get_success_url())

    
class ProfileDetailView(DetailView):
    model=Profile
    template_name='account/profiledetail.html'

    def get_object(self):
        return get_object_or_404(Profile,user__username=self.kwargs['username'])