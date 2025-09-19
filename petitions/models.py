from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    movie_title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.ManyToManyField(User, related_name='voted_petitions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_title
