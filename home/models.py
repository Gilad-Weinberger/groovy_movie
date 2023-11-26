from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db import models
from django.core.validators import FileExtensionValidator
import os

def actor_image_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"actor_{instance.actor_id}{ext}"
    return os.path.join('actors_images', new_filename)

def trailer_video_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"trailer_{instance.movie_id}{ext}"
    return os.path.join('trailer_videos', new_filename)

def movie_image_upload_path(instance, filename):
    filename, ext = os.path.splitext(filename)
    new_filename = f"movie_{instance.movie_id}{ext}"
    return os.path.join('movies_images', new_filename)

class Actor(models.Model):
    actor_id = models.CharField(max_length=8, blank=True)
    name = models.CharField(max_length=80)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), default='M')
    birthDate = models.DateField(default='1970-01-01', null=True)
    deathDate = models.DateField(default='1970-01-01', null=True, blank=True)
    image = models.ImageField(
        null=True,
        upload_to=actor_image_upload_path, 
        default='actors_images/default_image.jpg',
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])]
    )

    def movies_played(self):
        actor_roles = ActorMovieRole.objects.filter(actors=self)
        movies_played = Movie.objects.filter(actor_roles__in=actor_roles).distinct()
        return movies_played

    def __str__(self):
        return f'{self.actor_id} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.actor_id:
            last_id = Actor.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(8)
            else:
                new_id = '00000001'
            self.actor_id = new_id
        super().save(*args, **kwargs)

class Category(models.Model):
    category_id = models.CharField(max_length=4, blank=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.category_id:
            last_id = Category.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(4)
            else:
                new_id = '0001'
            self.category_id = new_id
        super().save(*args, **kwargs)

class ActorMovieRole(models.Model):
    actormovierole_id = models.CharField(max_length=8, blank=True)
    actors = models.ManyToManyField(Actor, related_name='actor_roles')
    character = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.actormovierole_id} - {', '.join(actor.name for actor in self.actors.all())} - {self.character.split()[0]} {self.character.split()[-1]}"

    def save(self, *args, **kwargs):
        if not self.actormovierole_id:
            last_id = ActorMovieRole.objects.order_by('actormovierole_id').last()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(8)
            else:
                new_id = '00000001'
            self.actormovierole_id = new_id
        super().save(*args, **kwargs)

class Movie(models.Model):
    movie_id = models.CharField(max_length=6, blank=True)
    name = models.CharField(max_length=250)
    series = models.ForeignKey('Series', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    trailerVideo = models.FileField(
        null=True,
        upload_to=trailer_video_upload_path, 
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]
    )
    image = models.ImageField(
        null=True,
        upload_to=movie_image_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])]
    )
    fontFamily = models.CharField(max_length=100)
    ageLimit = models.CharField(max_length=10, blank=True, null=True)
    length = models.IntegerField()
    year = models.IntegerField()
    rating = models.FloatField()
    ratingsCount = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='movies')
    actor_roles = models.ManyToManyField(ActorMovieRole, related_name='actor_roles')

    def __str__(self):
        return f'{self.movie_id} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.movie_id:
            last_id = Movie.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(6)
            else:
                new_id = '000001'
            self.movie_id = new_id
        
        if self.ratingsCount is None:
            self.ratingsCount = 0
        
        super().save(*args, **kwargs)

class Series(models.Model):
    series_id = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def series_movies(self):
        movies_in_series = Movie.objects.filter(series=self)
        return movies_in_series

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Serieses"

    def save(self, *args, **kwargs):
        if not self.series_id:
            last_id = Movie.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(4)
            else:
                new_id = '0001'
            self.series_id = new_id
        super().save(*args, **kwargs)

