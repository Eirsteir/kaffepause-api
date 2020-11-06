from rest_framework import serializers

from kaffepause.users.serializers import UserSerializer

from .models import Relationship


class FriendshipSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    addressee = UserSerializer(read_only=True)

    class Meta:
        model = Relationship
        fields = (
            "requester",
            "addressee",
            "status",
        )
        read_only_fields = ("requester", "addressee")
