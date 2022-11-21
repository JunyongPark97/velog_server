
from rest_framework import serializers
from blog.models import Post, Tag


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "created_at", "owner"]



class BlogSerializerWithTags(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", "title", "created_at", "owner", "tag"]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]


class BlogSerializerWithTagsV2(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "created_at", "owner", "tag"]
