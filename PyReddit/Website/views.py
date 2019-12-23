from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import Post
from .forms import PostCreateForm


def home(request):
    context = {'posts': Post.objects.all(),
               'active': 'home'}
    return render(request, 'Website/home.html', context = context)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        return Post.objects.order_by('-date_posted').all()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.path == '/':
            context['active'] = 'home'
            context['posts'] = Post.objects.order_by('-date_posted')[:3]
        elif self.request.path == '/blogs/':
            context['title'] = 'Blogs'
            context['active'] = 'blogs'
        return context

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        return Post.objects.filter(author = self.request.user).all().order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['title'] = 'My Blogs'
        context['active'] = 'blogs'
        context['action'] = 'userblogs'
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Blogs'
        context['active'] = 'blogs'
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Blog'
        context['active'] = 'blogs'
        context['action'] = 'create'
        return context
    
    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Blog'
        context['active'] = 'blogs'
        context['action'] = 'update'
        return context
    
    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self, **kwargs):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete Blog'
        context['active'] = 'blogs'
        return context
    
    def test_func(self, **kwargs):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False