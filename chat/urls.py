from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index , name ='index'),
    path('index.html', views.index , name ='index'),
    path('register.html', views.register , name ='register'),
    path('chat.html', views.chat , name ='chat'),
    path('user_chat/chat.html', views.user_chat , name ='chat'),
    # path('search.html', views.search , name ='search'),
    path('user_chat/<email>', views.user_chat , name ='user_chat'),
    path('logout.html', views.logout , name ='logout'),
    # path('profile/<email>', views.profile , name ='profile'),
]

