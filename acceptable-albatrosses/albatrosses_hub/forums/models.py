from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"<{cls}: name={self.name!r} description={self.description!r}>"

    def __str__(self):
        return f"<self.__class__.__name__:{self.name!r}>"


class Post(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='posts',
                              on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='posts',
                                on_delete=models.CASCADE)
    content = models.TextField(max_length=4000)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"<{cls}: board={self.board!r} subject={self.subject!r} \
                starter={self.starter!r} last_updated={self.last_updated!r} \
                content={self.content!r}>"

    def __str__(self):
        return f"<self.__class__.__name__:{self.subject!r}>"

    def get_absolute_url(self):
        return reverse('board-detail',
                       kwargs={'board': self.board.name, 'pk': self.pk})


class Comment(models.Model):
    message = models.TextField(max_length=4000)
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments',
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+',
                                   on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('comment-detail',
                       kwargs={'board': self.post.board.name,
                               'post_pk': self.post.pk, 'pk': self.pk})

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
