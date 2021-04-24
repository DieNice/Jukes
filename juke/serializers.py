from django.contrib.auth.models import User
from rest_framework import serializers
from juke.models import Tweet
from juke.models import Follower


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_name', 'first_name']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'text', 'photo', 'created', 'author']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = []


class UserFollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ['follows', 'followed']


class UserFollowedSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ['follower', 'followed']
