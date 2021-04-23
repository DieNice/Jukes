from django.shortcuts import render
from rest_framework import viewsets
from juke.serializers import UserSerializer
from juke.serializers import TweetSerializer
from django.contrib.auth.models import User
from juke.models import Tweet


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'  # вместо /users/id - /users/username


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
