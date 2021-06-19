from django.urls import path

from jd import views

app_name = 'jd'

urlpatterns = [
    path('', views.index, name='index')
]
