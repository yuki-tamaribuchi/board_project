from django.urls import path
from .views import SignUp,RegistProfileView

app_name='account'
urlpatterns = [
    path('signup/',SignUp.as_view(),name='signup'),
    path('signup/registprofile/',RegistProfileView.as_view(),name='registprofile'),
]
