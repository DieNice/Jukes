"""Jukes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter
from juke import views
from juke.router import SwitchDetailRouter

router = ExtendedDefaultRouter()
switchRowter = SwitchDetailRouter()

user_route = router.register(r'users', views.UserViewSet)
user_route.register(r'tweets', views.UserTweetViewSet, 'user-tweets', ['username'])
user_route.register(r'follows', views.UserFolowsViewSet, 'user-follows', ['username'])
user_route.register(r'followed', views.UserFollowedViewSet, 'user-followed', ['username'])
router.register(r'tweets', views.TweetViewSet)
router.register(r'feed', views.FeedViewSet)
switchRowter.register(r'follow', views.FollowUserViewSet)

urlpatterns = [
    path('v1/', include(switchRowter.urls)),
    path('v1/', include(router.urls)),
    path('/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
