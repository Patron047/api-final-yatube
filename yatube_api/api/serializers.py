from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Текст не может быть пустым.')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'created', 'post')
        read_only_fields = ('author', 'post', 'created')

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Текст не может быть пустым.')
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        if Follow.objects.filter(user=user, following=value).exists():
            raise serializers.ValidationError('Вы уже подписаны.')
        return value

    def create(self, validated_data):
        return super().create({
            **validated_data,
            'user': self.context['request'].user
        })
