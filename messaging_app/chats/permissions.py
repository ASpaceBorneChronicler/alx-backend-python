from rest_framework.permissions import BasePermission, IsAuthenticated

class IsInConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all() and IsAuthenticated().has_object_permission(request, view, obj)