# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

# The variable MUST be named exactly 'urlpatterns' (plural, lowercase)
urlpatterns = [
    # API Endpoints
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('chat/', views.ChatAPIView.as_view(), name='chat'),
    path('chat-history/', views.ChatHistoryView.as_view(), name='chat_history'),

    # Frontend Interface (The new line you added)
    path('interface/', views.frontend_view, name='frontend'),
]