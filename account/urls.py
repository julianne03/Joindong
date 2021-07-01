from django.urls import path
from django.contrib.auth import views as auth_views
from account import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile_signup/', views.profile_signup, name='profile_signup'),
    path('update/user/<str:user_name>/', views.update_user, name='update_user'),
    path('delete/user/<str:user_name>/', views.delete_user, name='delete_user'),
    path('serach/user/', views.search_user, name='search_user')
]
