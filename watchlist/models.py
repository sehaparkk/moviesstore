from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-rating']

    def __str__(self):
        return f'{self.user.username} - {self.movie.name} ({self.rating} stars)'