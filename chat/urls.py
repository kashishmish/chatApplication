# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('personal_chat',views.show_users,name='show_users'),
    path('groups',views.groups,name='groups'),
    path('chat/<str:room_name>', views.room, name='room'),
    path('personalchat/<str:you>', views.personal, name='personalroom'),
    path('profile',views.profile,name="profile"),
    path('remove_profile',views.remove_profile,name="remove_pic"),
    path('delete_user/<str:username>',views.delete_user,name="delete_user"),
    path('change_password',views.change_password,name="change_password"),
    path('otp_mail',views.otp_mail,name="otp_mail"),
]