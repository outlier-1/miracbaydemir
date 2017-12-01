from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Categories
from .forms import PostCreateForm
# Create your views here.


class HomeListView(ListView):
    template_name = "posts/post_base.html"
    model = Post

    def get_context_data(self,**kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        qs = Post.objects.all().order_by('-timestamp')[:5]
        context["latest"] = qs
        return context


class PostListView(ListView):
    template_name = "posts/post_list.html"
    model = Post
   
    def get_context_data(self,**kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            qs_filter = Post.objects.filter(categories__category_name__iexact=slug)
        else:
            qs_filter = Post.objects.none()
        qs = Post.objects.all().order_by('-timestamp')[:5]
        context["latest"] = qs
        context["articles"] = qs_filter
        return context


class PostDetailView(DetailView):
    template_name = "posts/post_detail.html"
    model = Post
    def get_context_data(self,**kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)        
        qs = Post.objects.all().order_by('-timestamp')[:5]
        context["latest"] = qs
        query = Post.objects.filter(categories__category_name__iexact=context["post"].categories)
        context["articles"] = query
        # print(context) FOR DEBUG!
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'posts/post_form.html'
    success_url   = '/posts/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "New Post"
        return context

