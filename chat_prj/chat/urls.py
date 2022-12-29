from django.urls import include, path
from rest_framework import routers

from .views import ChatRoomViewSet, ChatUserViewSet, index, ChatRoomView, ChatRoomList


router = routers.DefaultRouter()
router.register(r'chat_room', ChatRoomViewSet)
router.register(r'chat_user', ChatUserViewSet)

urlpatterns = [
    path('', index, name='chat'),
    path('<int:pk>/', ChatRoomView.as_view(), name='chat_room'),
    path('list/', ChatRoomList.as_view(), name='chat_room_list'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
