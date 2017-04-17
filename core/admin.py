from django.contrib import admin
from django.contrib.auth.models import User
from core.models import Content, Comments, Reviews

# Register your models here.
class CommentsInline(admin.StackedInline):
    model = Comments
    verbose_name_plural = 'Комментарии'

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published_at', 'like', 'dislike',)
    list_per_page = 10
    list_filter = ('author', )
    inlines = (CommentsInline, )

class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    verbose_name_plural = 'Отклики'

admin.site.register(Content, ContentAdmin)
admin.site.register(Reviews, ReviewsAdmin)
