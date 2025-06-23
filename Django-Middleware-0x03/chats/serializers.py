from rest_framework import serializers
from .models import Conversation, Message , User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'date_joined', 
            'last_login'
        ] 
        read_only_fields = [
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'date_joined', 
            'last_login', 
            'id', 
            'username', 
            'email' 
        ] 
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class MessageSerializer(serializers.ModelSerializer):

    conversation = serializers.StringRelatedField(read_only=True)
    sender = serializers.StringRelatedField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        Overrides the default __init__ to limit the conversations a user can post to
        to only the ones they are a participant of. This is done by filtering the queryset
        of the conversation field in the serializer when the request is given in the context.
        """
        super().__init__(*args, **kwargs)
        if self.context.get('request'):
            user = self.context['request'].user
            self.fields['conversation'].queryset = Conversation.objects.filter(
                participants=user
            )
    
    class Meta:
        model = Message
        fields = ['content', 'date_sent', 'sender', 'conversation']
        read_only_fields = ['sender', 'date_sent']

    def create(self, validated_data):
        
        """
        Overridden method to handle the creation of a new message instance.
        This method sets the sender of the message to the current authenticated user
        before saving the instance. This ensures that the sender_id field is filled
        and the user is a participant in the conversation.
        
        Args:
            validated_data: The validated message data.
        
        Returns:
            The created message instance.
        """
        validated_data['sender'] = self.context['request'].user 
        # To ensure the sender_id field is filled

        if validated_data['sender'] not in validated_data['conversation'].participants.all():
            raise serializers.ValidationError("You are not a participant in this conversation")
        return super().create(validated_data)
    
    
    

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['participants', 'messages', 'last_updated']
        read_only_fields = ['last_updated', 'messages']

    def create(self, validated_data):

        """
        Override the default create method to ensure the authenticated user
        is included as a participant in the conversation. If the user is not
        already in the participants list of the validated data, they are added
        before calling the superclass's create method.

        Args:
            validated_data: The validated conversation data.
        
        Returns:
            The created conversation instance.
        """

        if self.context['request'].user not in validated_data['participants']:
            validated_data['participants'].append(self.context['request'].user)

        return super().create(validated_data)
    
    
