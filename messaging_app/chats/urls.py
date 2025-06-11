from rest_framework import routers
from django.urls import path, include
from . import views


router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)
# router.register(r'user', views.UserViewSet)
router.register(r'conversations', views.ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]