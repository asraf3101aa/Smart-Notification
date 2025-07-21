from rest_framework import generics, permissions
from thread.serializers.thread_serializers import ThreadSerializer
from thread.models.thread_models import Thread


class ThreadCreateView(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)