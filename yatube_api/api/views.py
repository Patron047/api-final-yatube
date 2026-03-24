from rest_framework import viewsets, permissions, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def _get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self._get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self._get_post()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class FollowViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.followers.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
