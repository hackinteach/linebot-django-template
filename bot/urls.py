from django.urls import path
from . import views
urlpatterns = [
    path('', views.callback, name='callback'),
    path('send/', views.send_message, name='send_message'),
    path('health/', views.health, name='health')
]