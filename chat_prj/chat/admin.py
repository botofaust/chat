from django.contrib import admin

from . import models

admin.site.register(models.ChatUser)
admin.site.register(models.ChatRoom)
admin.site.register(models.ChatMessage)
