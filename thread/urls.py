from django.urls import path
from thread.views.comment_views import CommentListCreateView,CommentDetailView
from thread.views.thread_views import ThreadDetailView, ThreadListCreateView, ThreadSubscribeView

urlpatterns = [
    path('', ThreadListCreateView.as_view(), name='thread'),
    path('<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('<int:thread_id>/comment/', CommentListCreateView.as_view(), name='thread_list_create'),
    path('<int:thread_id>/comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('<int:thread_id>/subscribe/', ThreadSubscribeView.as_view(), name='thread_subscribe'),
]
