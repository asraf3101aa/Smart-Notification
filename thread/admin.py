from django.contrib import admin
from thread.models.thread_models import Thread
from thread.models.comment_models import Comment

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('created_at', 'updated_at')
    filter_horizontal = ('subscribers',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'short_text',
        'thread_title',
        'thread_created_by',
        'created_by',
        'created_at',
        'updated_at'
    )
    search_fields = (
        'text',
        'created_by__username',
        'thread__title',
        'thread__created_by__username'
    )
    list_filter = ('created_at', 'updated_at', 'thread')

    def short_text(self, obj):
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")
    short_text.short_description = 'Comment'

    def thread_title(self, obj):
        return obj.thread.title
    thread_title.short_description = 'Thread Title'

    def thread_created_by(self, obj):
        return obj.thread.created_by.username
    thread_created_by.short_description = 'Thread Created By'