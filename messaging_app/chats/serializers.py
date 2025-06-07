from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

#  TODO : Fix this  ... Updates n' shit
class ConversationSerializer(serializers.ModelSerializer):

    user_1 = UserSerializer(read_only=True)
    user_2 = UserSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'