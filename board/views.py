from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,View
from .models import Topic,Reply,Like
from django.urls import reverse_lazy,reverse
from .forms import TopicCreateForm
from django.http import HttpResponseRedirect
from account.models import Profile,Follow
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexView(TemplateView):
    template_name='board/index.html'


class IndexListView(LoginRequiredMixin,ListView):
    model=Topic
    context_object_name='topics'
    template_name='board/indexlist.html'

    def get_queryset(self):
        followed_user=Follow.objects.filter(following_user__user=self.request.user).values_list('followed_user',flat=False)
        reply_topics=Reply.objects.all().values_list('reply_from',flat=False)
        queryset=Topic.objects.filter(user__user__in=followed_user).exclude(id__in=reply_topics).order_by('-id')
        return queryset

    

class TopicDetailView(DetailView):
    model=Topic
    template_name='board/detail.html'
    context_oject_name='topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_topic=Topic.objects.get(pk=self.kwargs['pk'])
        reply_from_ids=Reply.objects.filter(reply_to_id=this_topic.id).values_list('reply_from',flat=False)
        context['replies']=Topic.objects.filter(id__in=reply_from_ids).order_by('-id')
        user=Profile.objects.get(user=self.request.user)
        context['liked']=Like.objects.filter(topic=this_topic,user=user)
        return context


class TopicCreateView(LoginRequiredMixin,CreateView):
    form_class=TopicCreateForm
    template_name='board/topiccreate.html'

    
    def post(self,request):
        form=TopicCreateForm(request.POST)

        new_topic=form.save(commit=False)
        new_topic.user=Profile.objects.get(id=request.user.id)
        new_topic.save()

        url=reverse_lazy('board:indexlist')
        return HttpResponseRedirect(url)


class ReplyCreateView(CreateView):
    form_class=TopicCreateForm
    template_name='board/replycreate.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.filter(pk=self.kwargs['pk'])
        return context


    def post(self,request,pk):
        form=TopicCreateForm(request.POST)
        new_topic=form.save(commit=False)
        new_topic.user=Profile.objects.get(id=request.user.id)
        new_topic.save()
        Reply.objects.create(reply_to=Topic.objects.get(pk=self.kwargs['pk']),reply_from=Topic.objects.get(pk=new_topic.id))

        url=reverse_lazy('board:indexlist')
        return HttpResponseRedirect(url)


class TopicDeleteView(LoginRequiredMixin,DeleteView):
    model=Topic

    def get_object(self):
        delete_object=Topic.objects.get(pk=self.kwargs['pk'])
        if delete_object.user.user.username==str(self.request.user):
            return delete_object
        else:
            return None

    def get_success_url(self):
        return reverse('account:detail',kwargs={'username':self.request.user})



class LikeProcess(LoginRequiredMixin,View):

    def get(self,request,**kwargs):
        user=Profile.objects.get(user=self.request.user)
        topic=Topic.objects.get(pk=self.kwargs['pk'])
        like=Like.objects.filter(user=user,topic=topic)
        if like.exists():
            like.delete()
        else:
            
            Like.objects.create(user=user,topic=topic)
        return redirect('board:detail',pk=self.kwargs['pk'])