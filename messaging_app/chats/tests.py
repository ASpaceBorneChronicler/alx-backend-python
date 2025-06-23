from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import User, Conversation, Message

# Create your tests here.

class ConversationTest(TestCase):


    def setUp(self):
    # Add things to db and 
        user1 = User.objects.create_user(username='username1', email='email1@gmail.com', password='password', first_name='first_name', last_name='last_name')
        user2 = User.objects.create_user(username='username2', email='email2@gmail.com', password='password', first_name='first_name', last_name='last_name')
        user3 = User.objects.create_user(username='username3', email='email3@gmail.com', password='password', first_name='first_name', last_name='last_name')
        

        convesation = Conversation.objects.create()
        convesation.participants.set([user1, user2])

    def test_conversation_permissions_when_logged_in(self):
    # Do the test
        user = User.objects.get(username='username1')
        self.client.force_login(user)
        
        url = reverse('conversation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_conversation_permissions_when_not_logged_in(self):
        url = reverse('conversation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_conversation_permissions_when_logged_in_as_another_user(self):
        user = User.objects.get(username='username3')
        self.client.force_login(user)
        
        url = reverse('conversation-list')
        response = self.client.get(url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_JWT_authentication(self):
        user = User.objects.get(username='username1')
        self.client.force_login(user)

        response = self.client.post('/api/token/', {'username': 'username1', 'password': 'password'})

        self.assertContains(response, 'access')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def tearDown(self):
        pass
    # Clean up db