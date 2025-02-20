from django.db import models
from django.db.models import Avg

class Director(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    durations = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE,related_name='movies')

    def __str__(self):
        return self.title

    
STARS = (
    (1,'*'),
    (2,'**'),
    (3,'***'),
    (4,'****'),
    (5,'*****'),
)
class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name='reviews')
    stars = models.PositiveIntegerField(null=True,choices=STARS)

    def __str__(self):
        return f"Отзыв к {self.movie.title}- {self.text}"
    
    