from django.db import models
from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    text = models.TextField(max_length=500)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_post',
        blank=True
    )

    class Meta:
        ordering = ['-posting_date']

    def __str__(self):
        return f'Post de {self.user.email} em {self.posting_date.strftime("%d/%m/%Y %H:%M")}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comentário de {self.user} no post'