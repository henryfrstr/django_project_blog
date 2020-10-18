from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class NewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()
    newmanager = NewManager()

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.title

    # @property
    # def published(self):
    #     if self.status == 'published':
    #         return True
    #     return False
