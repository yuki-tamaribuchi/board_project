from django.urls import path
from .views import IndexView,IndexListView

app_name='board'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('indexlist/',IndexListView.as_view(),name='indexlist'),
]
