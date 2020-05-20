from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from .models import Post, Comment
from .forms import CommentCreateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


def detail_view(request, pk):
    object = get_object_or_404(Post, pk=pk)
    form = CommentCreateForm(request.POST or None)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.author = request.user
                form.instance.post = object
                form.save()
                next = request.META.get('HTTP_REFERER', None) or '/'
                response = redirect(next)
                return response
        else:
            return redirect('/login/?next=%s' % request.path)

    context = {
        'object': object,
        'form': form
    }

    return render(request, 'blog/post_detail.html', context)

def test(request):
    content = {
        'posts': Post.objects.all(),
        'latest': Post.objects.order_by('-date_posted')[0],
    }
    return render(request, 'blog/test.html', content)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        latest = Post.objects.order_by('-date_posted')[0]
        context = super().get_context_data(**kwargs)
        context['latest'] = latest
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        latest = Post.objects.order_by('-date_posted')[0]
        context = super().get_context_data(**kwargs)
        context['latest'] = latest
        return context


class PostLikesToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = get_object_or_404(Post, pk=pk)
        user = self.request.user

        if user in object.likes.all():
            object.likes.remove(user)
        else:
            if user in object.dislikes.all():
                object.dislikes.remove(user)
            object.likes.add(user)

        return self.request.META.get('HTTP_REFERER')


class PostDislikesToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = get_object_or_404(Post, pk=pk)
        user = self.request.user

        if user in object.dislikes.all():
            object.dislikes.remove(user)
        else:
            if user in object.likes.all():
                object.likes.remove(user)
            object.dislikes.add(user)

        return self.request.META.get('HTTP_REFERER')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'images']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'images']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        messages.success(self.request, 'Your comment has been removed!')
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False
