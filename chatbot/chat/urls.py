from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.chat_api, name='chat_api'),  # API endpoint
    path('', views.chat_interface, name='chat_interface'),  # Chat interface
]
