from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Movie, ActorMovieRole, Category, Actor

class MovieForm(forms.ModelForm):
    actor_roles = forms.ModelMultipleChoiceField(
        queryset=ActorMovieRole.objects.all(),
        widget=FilteredSelectMultiple("Actor Movie Roles", is_stacked=False),
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=FilteredSelectMultiple("Categories", is_stacked=False),
    )

    class Meta:
        model = Movie
        fields = '__all__'

class ActorMovieRoleForm(forms.ModelForm):
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        widget=FilteredSelectMultiple("Actors", is_stacked=False),
    )

    class Meta:
        model = ActorMovieRole
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['actors'].widget.can_add_related = False  # Disable adding new actors
            self.fields['actors'].widget.can_change_related = False  # Disable changing the selected actor
            self.fields['actors'].widget.can_delete_related = False  # Disable removing the selected actor
            self.fields['actors'].widget.attrs['size'] = 1  # Set the size of the select box to 1

class ActorForm(forms.ModelForm):
    movies_played = forms.ModelMultipleChoiceField(queryset=Movie.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['movies_played'].queryset = self.instance.movies_played()

class SeriesForm(forms.ModelForm):
    movies = forms.ModelMultipleChoiceField(queryset=Movie.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['movies'].queryset = self.instance.movies.all()