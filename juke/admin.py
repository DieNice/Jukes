from django.contrib import admin

from .models import Tweet, Follower

admin.site.register(Tweet)
admin.site.register(Follower)
