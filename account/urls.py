from django.urls import path
from .views import SignUp,RegistProfileView,ProfileDetailView,LoginView,ProfileUpdateView,AccountManageView,FollowingListView,FollowerListView
from django.contrib.auth import views as auth_views

app_name='account'
urlpatterns = [
    path('signup/',SignUp.as_view(),name='signup'),
    path('signup/registprofile/',RegistProfileView.as_view(),name='registprofile'),
    path('<str:username>/detail/',ProfileDetailView.as_view(),name='detail'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('update/',ProfileUpdateView.as_view(),name='update'),
    path('manage/',AccountManageView.as_view(),name='manage'),
    path('<str:username>/following/',FollowingListView.as_view(),name='followinglist'),
    path('<str:username>/follower/',FollowerListView.as_view(),name='followerlist'),
]
