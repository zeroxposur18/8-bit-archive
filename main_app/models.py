from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

ESRB = (
    ('E', 'Everyone'),
    ('T', 'Teen'),
    ('M', 'Mature'),
)

GENRES = (
    ('FPS', 'First-person Shooter'),
    ('Action', 'Action'),
    ('Platformer', 'Platformer'),
    ('Adventure', 'Adventure'),
    ('RPG', 'Role-play Game'),
    ('Racing', 'Racing'),
    ('Puzzle', 'Puzzle'),
    ('Strategy', 'Strategy'),
)

class Game(models.Model):
    title = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    year = models.DateField('release date')
    genre = models.CharField(
        max_length=50,
        choices=GENRES,
        default = GENRES[0][0])
    esrb = models.CharField(
        max_length=50,
        choices=ESRB,
        default= ESRB[0][0])
    publisher = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("games_detail", kwargs={"game_id": self.id})
    
class Collection(models.Model):
    title = models.CharField(max_length=50)
    games = models.ManyToManyField(Game)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs = {"collection_id": self.id})

# class Photo(models.Model):
#   url = models.CharField(max_length=200)
#   collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
#   def __str__(self):
#       return f"Photo for collection_id: {self.collection_id} @{self.url}"

# class Sighting(models.Model):
#     date = models.DateField('sighting date')
#     spot = models.CharField(
#         max_length=1,
#         choices=SPOTS,
#         default=SPOTS[0][0]
#     )
#     finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.get_spot_display()} on {self.date}"
    
#     class Meta:
#         ordering = ['-date']
