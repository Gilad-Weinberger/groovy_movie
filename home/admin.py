from django.contrib import admin
from .models import Movie, Category, Actor, ActorMovieRole, Series
from .forms import MovieForm, ActorMovieRoleForm, ActorForm, SeriesForm

class MovieAdmin(admin.ModelAdmin):
    form = MovieForm
    list_display = ('movie_id', 'name', 'series', 'year', 'rating', 'ratingsCount', 'length')
    list_filter = ('series', 'year', 'series', 'rating')

    actions = ['duplicate_selected']

    def duplicate_selected(self, request, queryset):
        for movie in queryset:
            new_movie = movie
            new_movie.pk = None
            new_movie.movie_id = None
            new_movie.name = f"{movie.name} (Copy)"
            new_movie.save()

        self.message_user(request, f"{len(queryset)} movies duplicated successfully.")
    
    duplicate_selected.short_description = "Duplicate selected movies"


class ActorMovieRoleAdmin(admin.ModelAdmin):
    form = ActorMovieRoleForm
    list_display = ('actormovierole_id', 'get_actor_names', 'character')
    
    def get_actor_names(self, obj):
        return ', '.join(actor.name for actor in obj.actors.all())
    get_actor_names.short_description = 'Actors'


class SeriesAdmin(admin.ModelAdmin):
    form = SeriesForm
    list_display = ('series_id', 'name', 'description')

class ActorAdmin(admin.ModelAdmin):
    form = ActorForm
    list_display = ('actor_id', 'name', 'gender')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(ActorMovieRole, ActorMovieRoleAdmin)
admin.site.register(Series, SeriesAdmin)
