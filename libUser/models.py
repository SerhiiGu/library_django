from django.db import models
from django.contrib.auth.models import User


class Books(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    all_count = models.IntegerField()
    free_count = models.IntegerField()
    users_use = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return f'{self.author} : {self.title}'


class UserBooks(models.Model):
    RANG_CHOICES = (
        (0, 'readed'),
        (1, 'reading'),
        (2, 'request to read')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=RANG_CHOICES)

    def __str__(self):
        return f'{self.user} {self.book}'


class NewBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.author} {self.title}'


class BooksHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    dt_start = models.DateTimeField(auto_now_add=True)
    dt_end = models.DateTimeField(blank=True)

    def __str__(self):
        return f'{self.user} {self.book}'
