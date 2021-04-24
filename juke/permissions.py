from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from .models import Tweet, Follower


# Определили свой Persmission
class IsTweetAuthorOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj: Tweet):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            obj.author == request.user
        )


class IsFollowUserOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    # Проверка прав для конкретного объекта
    def has_object_permission(self, request, view, obj: Follower):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and obj.author == request.user
        )
