from django.shortcuts import render
from django.views.generic.edit import CreateView,DeleteView
from .forms import SignUpForm,RegistProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect

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