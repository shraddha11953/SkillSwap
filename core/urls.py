from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('exchange/', views.exchange_request, name='exchange'),
    path('chat/', views.chat, name='chat'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('get-events/', views.get_events, name='get_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('test/',views.test,name='test'),
    #path("ws/", include("core.routing.websocket_urlpatterns")),


]
