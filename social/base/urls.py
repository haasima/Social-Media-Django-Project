from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView,
    PostDeleteView, postLike
)
from . import views

app_name = 'base'

urlpatterns = [
    # Post
    #  path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('', PostListView.as_view(), name='home'),
    path('post/<slug:slug>/<int:year>/<int:month>/<int:day>/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # Like posts
    path('post-like/<int:pk>', views.postLike, name='post-like'),
    # About page
    path('about/', views.about, name="about"),
]
