from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from .models import Topic
from django.urls import reverse_lazy
from .forms import TopicCreateForm
from django.http import HttpResponseRedirect
from account.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

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


class TopicCreateView(CreateView,LoginRequiredMixin):
    form_class=TopicCreateForm
    template_name='board/topiccreate.html'
    
    def post(self,request):
        form=TopicCreateForm(request.POST)

        new_topic=form.save(commit=False)
        new_topic.user=Profile.objects.get(id=request.user.id)
        new_topic.save()
        url=reverse_lazy('board:indexlist')
        return HttpResponseRedirect(url)