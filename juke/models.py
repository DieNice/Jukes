from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=100)
    photo = models.URLField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.author.username}]{self.text}'
