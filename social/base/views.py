from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

# drf
from django.db.models import Prefetch, Count, Exists, Case, When, BooleanField

# Views and Forms
from .forms import CommentForm
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
# Redis  
import redis
from django.conf import settings
from django.views.decorators.cache import cache_page

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def postLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('base:post-detail', kwargs={'slug': post.slug,
                                                                    'year': post.date_posted.year,
                                                                    'month': post.date_posted.month,
                                                                    'day': post.date_posted.day, 'pk': post.pk}))


class PostListView(ListView):
    model = Post
    template_name = 'base/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        queryset = (super().get_queryset().select_related('author__profile')
                    .only('title', 'slug', 'content', 'date_posted', 'author__username', 'author__profile__image'))
        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self) -> bool | None:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()

        # post url
        year, month, day, slug = (self.kwargs["year"],
                                  self.kwargs["month"],
                                  self.kwargs["day"], self.kwargs["slug"])
        # slug = self.kwargs["slug"]

        post = get_object_or_404(Post.objects.select_related('author__profile')
                                 .only('title', 'slug', 'content', 'date_posted', 'author__profile__image',
                                       'author__username'),
                                 slug=slug, date_posted__year=year,
                                 date_posted__month=month, date_posted__day=day)
        # comments
        comments = post.comments.select_related('username__profile') \
            .only('post_id', 'username__username', 'content', 'created', 'username__profile__image') \
            .filter(active=True)

        context['comments'] = comments
        context['form'] = CommentForm()
        context['users'] = users

        # like posts
        likes_connected = post
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['number_of_likes'] = likes_connected.likes.count()
        context['post_is_liked'] = liked

        # views
        total_views = r.incr(f"post:{post.id}:views")
        context['total_views'] = total_views

        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = self.object

        comments = post.comments.select_related('username__profile') \
            .only('post_id', 'username__username', 'content', 'created', 'username__profile__image') \
            .filter(active=True)

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                username=request.user, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form

            return self.render_to_response(context=context)

        return self.render_to_response(context=context)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset().select_related('author__profile')
        # queryset = queryset.prefetch_related(Prefetch('comments', Comment.objects.select_related('username__profile')))
        return queryset


def about(request):
    return render(request, 'base/about.html', {'title': 'About'})
