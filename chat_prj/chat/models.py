import datetime

from django.contrib.auth.models import User
from django.db import models


class ChatUser(models.Model):
    nickname = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, default='<Без имени>')
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name='owner')
    members = models.ManyToManyField(ChatUser)


class ChatMessage(models.Model):
    text = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chat = models.ForeignKey(ChatRoom, default=1, on_delete=models.CASCADE)
    owner = models.ForeignKey(ChatUser, on_delete=models.CASCADE)

    def get_text_for_chat(self):
        date = self.created_at.strftime('%d.%m %H:%M')
        return f'{date} {self.owner.nickname}: {self.text}'
