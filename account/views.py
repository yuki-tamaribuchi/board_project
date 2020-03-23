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
from board.models import Topic,Reply


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
    context_object_name='profile'

    def get_object(self):
        return get_object_or_404(Profile,user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #トピック一覧の取得(返信含む)
        context['topics_w_reply']=Topic.objects.filter(user__user__username=self.kwargs['username']).order_by('-id')

        #フォロー数・フォロワー数の取得
        context['following_count']=Follow.objects.filter(following_user__user__username=self.kwargs['username']).count()
        context['followed_count']=Follow.objects.filter(followed_user__user__username=self.kwargs['username']).count()
        
        #フォロー中であるかを取得
        followed_user=get_object_or_404(Profile,user__username=self.kwargs['username'])
        following_user=get_object_or_404(Profile,user__username=self.request.user)
        context['is_following']=Follow.objects.filter(followed_user__user__username=followed_user,following_user__user=self.request.user)
        
        #自分自身をフォローしないようにするための本人確認データの取得
        if followed_user==following_user:
            context['is_sameuser']=True
        else:
            context['is_sameuser']=False

        return context

        

class LoginView(View):
    def post(self,request,*arg,**kwargs):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            user=User.objects.get(username=username)
            login(request,user)
            return redirect('board:indexlist')
        return render(request,'account/login.html',{'form':form,})

    def get(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        return render(request,'account/login.html',{'form':form,})


class ProfileUpdateView(LoginRequiredMixin,UpdateView):
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

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        getusername=Profile.objects.get(user__username=self.kwargs['username'])
        context['username']=self.kwargs['username']
        context['userhandle']=getusername.handle
        print("Context=",context)
        return context
    
        
class FollowerListView(ListView):
    model=Follow
    template_name='account/followerlist.html'
    context_object_name='follower'

    def get_queryset(self):
        queryset=Follow.objects.filter(followed_user__user__username=self.kwargs['username'])
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        getusername=Profile.objects.get(user__username=self.kwargs['username'])
        context['username']=self.kwargs['username']
        context['userhandle']=getusername.handle
        return context



class FollowProcess(LoginRequiredMixin,View):
    

    def get(self,request,username,**kwargs):
        followed_user=get_object_or_404(Profile,user__username=self.kwargs['username'])
        following_user=get_object_or_404(Profile,user__username=self.request.user)
        follow=Follow.objects.filter(followed_user__user__username=followed_user,following_user__user=self.request.user)
        
        if followed_user==following_user:
            return redirect('account:detail',username=self.kwargs['username'])
        else:
            if follow.exists():
                follow.delete()
            else:
                Follow.objects.create(followed_user=followed_user,following_user=following_user)
            return redirect('account:detail', username=self.kwargs['username'])