from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):

    class NewManager(models.Manager):

        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
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


class Comment(models.Model):

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return f"Comment by {self.name}"
