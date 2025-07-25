from django.shortcuts import get_object_or_404
from thread.models.comment_models import Comment
from thread.serializers.comment_serializers import CommentSerializer
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from thread.models.thread_models import Thread
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.throttling import UserRateThrottle


class CommentListCreateView(ListCreateAPIView):
    """
    API view to list all comments created by the requesting user 
    within a specific thread and allow the user to create new comments 
    in that thread.
    """
    serializer_class = CommentSerializer
    permission_classes = [DjangoModelPermissions]
    throttle_scope = 'user'

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)
        return Comment.objects.filter(thread=thread, created_by=self.request.user)

    def perform_create(self, serializer):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)
        serializer.save(created_by=self.request.user, thread=thread)

    def get_throttles(self):
        if self.request.method == 'POST':
            throttle = UserRateThrottle()
            throttle.scope = self.throttle_scope
            return [throttle]
        return []

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific comment 
    created by the requesting user within a specific thread.
    """
    serializer_class = CommentSerializer 
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)
        return Comment.objects.filter(thread=thread, created_by=self.request.user)