from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Playlist
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  )
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user


class CustomUserProfileUpdateForm(forms.ModelForm):
    favorite_genre = forms.ChoiceField(
        choices=(
            ('Rock', 'Rock'),
            ('Pop', 'Pop'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Jazz', 'Jazz'),
            ('Classical', 'Classical'),
            ('Electronic', 'Electronic'),
            ('Country', 'Country'),
            ('Kpop', 'Kpop'),
    ),
        required=False,
        help_text='Select your favorite genre.'
    )

    class Meta:
        model = UserProfile
        fields = ('favorite_genre',)

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'songs', 'is_public']
        widgets = {
            'songs': forms.CheckboxSelectMultiple,
        }


class SongSearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    artist = forms.CharField(max_length=100, required=False)
    genre = forms.CharField(max_length=100, required=False)