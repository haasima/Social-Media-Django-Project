from django.contrib.auth.models import User
from rest_framework import viewsets
from base.models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrIsStaffOrReadOnly
from django.db.models import Count, Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(likes_count=Count('likes')).select_related('author')\
                .only('title', 'slug', 'author', 'date_posted', 'author__id')

    permission_classes = (IsOwnerOrIsStaffOrReadOnly,)
