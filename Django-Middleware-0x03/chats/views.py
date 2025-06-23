from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsInConversation

# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsInConversation]
    
    def get_queryset(self):
        """
        Overwrites the default get_queryset to only return conversations 
        that the requesting user is a participant of.
        """
        return super().get_queryset().filter(participants=self.request.user)




class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overridden method to handle the creation of a new message instance.
        This method sets the sender of the message to the current authenticated user
        before saving the instance.
        
        Args:
            serializer: The serializer instance used to validate and save the message data.
        """

        serializer.save(sender=self.request.user)
 