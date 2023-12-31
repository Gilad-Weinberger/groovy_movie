from django.shortcuts import render, get_object_or_404
from .models import Actor, ActorMovieRole, Category, Movie, Series
import random
from django.http import HttpRequest

def get_random_main_movie():
    movies = list(Movie.objects.all())
    if movies:
        return random.choice(movies)
    return None

def Home(request: HttpRequest):
    actors = list(Actor.objects.all())
    
    # main_movie_id = request.GET.get('mainMovie')
    
    # if main_movie_id:
    #     main_movie = Movie.objects.filter(movie_id=main_movie_id).first()
    # else:
    #     main_movie = get_random_main_movie()
    
    # main_series = main_movie.series

    video_source = ''
    length_in_hours = 0
    minutes = 0

    context = {
        'actors': actors,
        'videoSource': video_source,
        'lengthInHours': length_in_hours,
        'minutes': minutes,
    }

    # con = {
    #     'mainMovie': main_movie,
    #     'mainSeries': main_series,
    # }

    return render(request, 'home/home.html', context)

def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, actor_id=actor_id)
    return render(request, 'home/actor_detail.html', {'actor': actor})
