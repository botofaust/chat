from rest_framework import serializers

from .models import ChatRoom, ChatUser


class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['name', 'owner']


class ChatUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['nickname']
