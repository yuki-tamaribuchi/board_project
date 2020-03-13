from django.shortcuts import render,redirect
from django.views.generic import CreateView,DetailView,View,UpdateView,TemplateView,ListView
from .forms import SignUpForm,RegistProfileForm,LoginForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .models import Profile,Follow
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


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
        

class RegistProfileView(CreateView,LoginRequiredMixin):
    form_class=RegistProfileForm
    template_name='account/registprofile.html'
    success_url=reverse_lazy('account:manage')

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


class LoginView(View):
    def post(self,request,*arg,**kwargs):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            user=User.objects.get(username=username)
            login(request,user)
            return redirect('board:index')
        return render(request,'account/login.html',{'form':form,})

    def get(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        return render(request,'account/login.html',{'form':form,})


class ProfileUpdateView(UpdateView,LoginRequiredMixin):
    template_name='account/profileupdate.html'
    model=Profile
    fields=('handle','location','biograph')

    def get_object(self):
        return get_object_or_404(Profile,user__username=self.request.user)

    def get_success_url(self):
        return reverse('board:index')

    def get_form(self):
        form=super(ProfileUpdateView,self).get_form()
        form.fields['handle'].label='ハンドルネーム'
        form.fields['location'].label='場所'
        form.fields['biograph'].label='自己紹介'
        return form


class AccountManageView(TemplateView):
    template_name='account/accountmanage.html'


class FollowingListView(ListView):
    model=Follow
    template_name='account/followinglist.html'
    context_object_name='follow'

    def get_queryset(self):
        #queryset=Follow.objects.get(following_user__user__username=self.kwargs['username'])
        
        queryset=Follow.objects.filter(following_user__user__username=self.kwargs['username'])
        print(queryset)
        return queryset

    
        
        