from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from kaffepause.common.permissions import IsUserOrReadOnly

from .models import Relationship
from .serializers import FriendshipSerializer


class FriendshipViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Updates and retrieves friendships
    """

    queryset = Relationship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = (IsUserOrReadOnly,)


class FriendshipCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates friendships
    """

    queryset = Relationship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = (AllowAny,)
