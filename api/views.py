
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, ChatMessageSerializer
from .models import ChatMessage
from .rag_utils import get_rag_response

# 1. Register User
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Chat with RAG
class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated] # Requires JWT
    
    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({"error": "Message required"}, status=status.HTTP_400_BAD_REQUEST)

        # Call AI Pipeline
        ai_response = get_rag_response(user_message)

        # Save to DB
        ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=ai_response
        )

        return Response({"response": ai_response})

# 3. Get History
class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = ChatMessage.objects.filter(user=request.user).order_by('-created_at')
        serializer = ChatMessageSerializer(chats, many=True)
        return Response(serializer.data)
