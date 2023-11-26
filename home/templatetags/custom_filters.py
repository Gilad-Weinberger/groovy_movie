from django import template
register = template.Library()

@register.filter
def custom_mini_movie_name(movie_name, series_name):
    if movie_name.startswith(series_name):
        movie_name = movie_name[len(series_name):].lstrip()
        if movie_name.startswith("and the"):
            movie_name = movie_name[8:].lstrip()
        elif movie_name.startswith(": "):
            movie_name = movie_name[2:].lstrip()
    return movie_name
