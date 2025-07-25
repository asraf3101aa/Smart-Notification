from thread.serializers.thread_serializers import ThreadSerializer
from thread.models.thread_models import Thread
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from django.shortcuts import get_object_or_404


class ThreadListCreateView(ListCreateAPIView):
    """
    API view to list all threads created by the requesting user 
    and allow the user to create new threads.
    """
    serializer_class = ThreadSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Thread.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ThreadDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific thread 
    created by the requesting user.
    """
    serializer_class = ThreadSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Thread.objects.filter(created_by=self.request.user)


class ThreadSubscribeView(GenericAPIView):
    """
    API view to allow the requesting user to subscribe or unsubscribe 
    from a specific thread using POST (subscribe) and DELETE (unsubscribe) methods.
    """
    permission_classes = [DjangoModelPermissions]
    queryset = Thread.objects.all()
    
    def post(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, pk=kwargs['thread_id'])
        user = request.user

        if thread.subscribers.filter(id=user.id).exists():
            return Response({'detail': 'Already subscribed.'}, status=status.HTTP_400_BAD_REQUEST)

        thread.subscribers.add(user)
        return Response({'detail': 'Subscribed successfully.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, pk=kwargs['thread_id'])
        user = request.user

        if not thread.subscribers.filter(id=user.id).exists():
            return Response({'detail': 'Not subscribed to this thread.'}, status=status.HTTP_400_BAD_REQUEST)

        thread.subscribers.remove(user)
        return Response({'detail': 'Unsubscribed successfully.'}, status=status.HTTP_200_OK)