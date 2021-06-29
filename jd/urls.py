from django.urls import path

from jd import views

app_name = 'jd'

urlpatterns = [
    path('', views.index, name='index'),
    path('club_list/', views.club_list, name='club_list'),
    path('club/create/', views.create_club, name='club_create'),
    path('club/detail/<str:club_title>/', views.detail_club, name='club_detail'),
    path('club/modify/<str:club_title>/', views.update_club, name='club_update'),
    path('club/message/modify/<str:club_title>/', views.update_club_message, name='club_message_update'),
    path('club/<str:user_name>/', views.my_club, name='my_club'),
    path('mypage/<str:user_name>/', views.my_page, name='my_page'),
    path('club/apply/<str:club_title>/', views.apply_club, name='club_apply'),
    path('club/cancel/apply/<str:club_title>/', views.cancel_apply_club, name='club_cancel_apply'),
]
