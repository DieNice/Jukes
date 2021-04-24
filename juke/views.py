from django.shortcuts import render
from rest_framework import viewsets
from juke.serializers import UserSerializer, TweetSerializer, FollowSerializer, UserFollowsSerializer, \
    UserFollowedSerializer
from django.contrib.auth.models import User
from juke.models import Tweet, Follower
from .permissions import IsTweetAuthorOrReadOnly, IsFollowUserOrReadOnly
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'  # вместо /users/id - /users/username


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsTweetAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserTweetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(author__username=self.kwargs['parent_lookup_username'])


class FollowUserViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Follower.objects
    serializer_class = FollowSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follows = User.objects.get(username=self.kwargs[self.lookup_field])
        serializer.save(follower=self.request.user, follows=follows)

    def get_object(self):
        return self.queryset.filter(follower=self.request.user, follows__username=self.kwargs[self.lookup_field])


class FeedViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author__followers__follower__exact=self.request.user)


class UserFolowsViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Follower.objects
    serializer_class = UserFollowsSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follower__username=username)


class UserFollowedViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Follower.objects
    serializer_class = UserFollowedSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follows__username=username)
