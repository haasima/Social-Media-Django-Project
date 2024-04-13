from rest_framework import serializers

from base.models import Post


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'date_posted', 'likes_count')