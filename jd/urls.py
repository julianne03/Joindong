from django.urls import path

from jd import views

app_name = 'jd'

urlpatterns = [
    path('', views.index, name='index'),
    path('club_list/', views.club_list, name='club_list'),
    path('club/create/', views.create_club, name='club_create'),
    path('club/detail/<str:club_title>/', views.detail_club, name='club_detail'),
    path('club/modify/<str:club_title>/', views.update_club, name='club_update'),
    path('club/<str:user_name>/', views.my_club, name='my_club'),
]
