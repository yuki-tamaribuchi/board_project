from django.urls import path
from .views import IndexView,IndexListView,TopicDetailView,TopicCreateView,TopicDeleteView

app_name='board'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('indexlist/',IndexListView.as_view(),name='indexlist'),
    path('detail/<int:pk>/',TopicDetailView.as_view(),name='detail'),
    path('createtopic/',TopicCreateView.as_view(),name='create'),
    path('delete/<int:pk>/',TopicDeleteView.as_view(),name='delete'),
]
