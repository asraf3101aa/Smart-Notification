from django.urls import path
from thread.views.thread_views import ThreadCreateView

urlpatterns = [
    path('create', ThreadCreateView.as_view(), name='thread_create'),
]
