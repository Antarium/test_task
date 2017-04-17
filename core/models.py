from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ContentInfo(models.Model):
    class Meta:
        abstract = True
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.PositiveSmallIntegerField(default=0)
    dislike = models.PositiveSmallIntegerField(default=0)
    author = models.ForeignKey(User, blank=True, null=True)

class Content(ContentInfo):
    CONTENT_TYPE = (
        (0, 'статья'),
        (1, 'новость'),
    )
    class Meta:
        db_table = 'content'
        ordering = ['-published_at']
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'
    title = models.CharField(max_length=80)
    preview = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.SmallIntegerField(choices=CONTENT_TYPE, default=0)
    published_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.preview:
            self.preview = self.text[:200]
        super (Content, self).save(*args, **kwargs)

class Comments(ContentInfo):
    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    content = models.ForeignKey(Content)

class Reviews(models.Model):
    REVIEW_OF = (
        (0, 'статья'),
        (1, 'новость'),
    )
    user_id = models.PositiveIntegerField()
    content_id = models.PositiveIntegerField()
    content_type = models.SmallIntegerField(choices=REVIEW_OF)
    review = models.BooleanField(help_text='false - dislike; true - like')
