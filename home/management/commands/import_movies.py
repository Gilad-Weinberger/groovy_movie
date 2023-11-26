from django.core.management.base import BaseCommand
from home.models import Movie, Actor, Series
import os
import json

class Command(BaseCommand):
    help = 'Imports movies from JSON file'

    def handle(self, *args, **options):
        script_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_path, 'movies.json')

        # Create the series object
        series = Series.objects.create(name="Harry Potter")
        
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

            for movie_data in data['movies']:
                categories_data = movie_data.pop('categories')
                players_data = movie_data.pop('players')

                movie = Movie.objects.create(
                    name=movie_data['name'],
                    fontFamily=movie_data['fontFamily'],
                    description=movie_data['description'],
                    trailerVideo=None,
                    rating=movie_data['rating'],
                    length=movie_data['length'],
                    year=movie_data['year'],
                    ageLimit=movie_data.get('ageLimit', None),
                    series=series  # Use the created series object here
                )

                actors = []
                for player_data in players_data:
                    actor, created = Actor.objects.get_or_create(
                        name=player_data['name'],
                        gender="M",
                        birthDate=None,
                        deathDate=None,
                        image=None,
                    )
                    actors.append(actor)

                movie.categories.set(categories_data)
                movie.actor_roles.set(actors)

        self.stdout.write(self.style.SUCCESS('Successfully imported movies'))
