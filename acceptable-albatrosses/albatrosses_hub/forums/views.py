from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Board, Post, Comment


# Create your views here.
def forumspage(request):
    context = {'boards': Board.objects.all()}
    return render(request, "forums/forum.html", context)


class PostListView(ListView):
    model = Post
    paginate_by = 2
    template_name = 'forums/board.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.board = get_object_or_404(Board, name=self.kwargs['board'])
        return Post.objects.filter(board=self.board).order_by('-last_updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
                              post=context['post']).order_by('-created_at')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['subject', 'content']

    def form_valid(self, form):
        form.instance.starter = self.request.user
        form.instance.board_id = get_object_or_404(
                                 Board, name=self.kwargs['board']).id
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['subject', 'content']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.starter:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('board-view', kwargs={'board': self.kwargs['board']})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.starter:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'forums/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(starter=user).order_by('-last_updated')


class CommentDetailView(DetailView):
    model = Comment


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['message']

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.created_by:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('board-detail', kwargs={'board':
                       self.kwargs['board'], 'pk': self.kwargs['post_pk']})

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.created_by:
            return True
        return False
