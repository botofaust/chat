from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import viewsets

from .serializers import ChatRoomSerializer, ChatUserSerializer
from .consumers import ChatConsumer
from .models import ChatMessage, ChatRoom, ChatUser


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class ChatUserViewSet(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = ChatUserSerializer


def index(request):
    return render(request, 'chat/index.html')


class ChatRoomView(UserPassesTestMixin, DetailView):
    model = ChatRoom
    template_name = 'chat/chat_room.html'

    def test_func(self):
        user = ChatUser.objects.get(pk=self.request.user.pk)
        chatroom = self.get_object()
        return (user in chatroom.members.all()) or (user == chatroom.owner)


class ChatRoomList(ListView):
    model = ChatRoom
    template_name = 'chat/chat_room_list.html'


@receiver(post_save, sender=ChatMessage)
def send_messages_to_clients(sender, instance, **kwargs):
    sync_send = async_to_sync(ChatConsumer.send_to_chat)
    sync_send(instance.chat.id, instance.get_text_for_chat())
