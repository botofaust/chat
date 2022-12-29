from django.contrib import admin
from django.urls import include, path

from .views import index_view, login_view, logout_view

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]
