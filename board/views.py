from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from .models import Topic


# Create your views here.
class IndexView(TemplateView):
    template_name="board/index.html"


class IndexListView(ListView):
    model=Topic
    context_object_name='topics'
    template_name='board/indexlist.html'


class TopicDetailView(DetailView):
    model=Topic
    template_name='board/detail.html'
    context_oject_name='topic'
