from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

# User model

class User(AbstractUser):

    def __str__(self):
        return f'''{self.username}'''
    

# Conversation model

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    last_updated = models.DateTimeField(auto_now=True) # auto_now to track update times to convesation

    def __str__(self):
        participants_list = list(self.participants.all()[:2])
        if len(participants_list) >= 3:
            return f"Chat between {participants_list[0].username}, {participants_list[1].username} and ..."
        elif len(participants_list) == 2:
            return f"Chat between {participants_list[1].username} and {participants_list[0].username}"
        else:
            return "Empty Conversation"
        
# Message model

class Message(models.Model):
    content = models.CharField(verbose_name='message_contents', blank=True,)
    date_sent = models.DateTimeField(auto_now_add=True) # auto_now_add to track the creation time of the entry
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Message sent by {self.sender.username} at {self.date_sent}' 
        # DONE: make sure this is pulling from the User model
    

# TODO: See if choices field will help with conversation management/ message management