from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from .models import Topic

# Create your views here.
class IndexView(TemplateView):
    template_name="board/index.html"


class IndexListView(ListView):
    model=Topic
    context_object_name='topics'
    template_name='board/indexlist.html'