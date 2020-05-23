from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    images = models.ImageField(upload_to='post_pics', blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.images:
            img = Image.open(self.images.path)

            if img.height > 1600 or img.width > 1200:
                output_size = (1200, 1600)
                img.thumbnail(output_size)
                img.save(self.images.path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment of post-{self.post.pk} by {self.author.username}: {self.text}'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
