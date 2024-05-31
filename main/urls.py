from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('random-chat-enterance/',views.randomchat_enterance, name='random_chat_enter'),
    path('random-chat/',views.index, name='random_chat'),
    path('home/',views.home, name='home'),
    path('mychats/',views.mychats, name='mychats'),
    path('private-chat/<int:user_id>/', views.private_chat_view, name='private_chat'),

]
