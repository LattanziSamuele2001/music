from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
                                  TemplateView,DeleteView)
from .models import Song, Playlist, UserProfile
from .forms import (CustomUserCreationForm, PlaylistForm,
                    CustomAuthenticationForm,
                    CustomUserProfileUpdateForm,  SongSearchForm)
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from collections import Counter
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def recommend_songs_by_genre(profile):
    if profile.favorite_genre:
        favorite_genre = profile.favorite_genre
    else:
        favorite_genre = []
    recommended_songs = Song.objects.filter(genre=favorite_genre)
    return recommended_songs


def recommend_songs_by_artists(user):
    playlists = Playlist.objects.filter(user=user)
    artist_counter = Counter()
    for playlist in playlists:
        for song in playlist.songs.all():
            artist_counter[song.artist] += 1
    most_common_artist = artist_counter.most_common(1)
    if most_common_artist:
        most_common_artist = most_common_artist[0][0]
    recommended_songs = Song.objects.filter(artist=most_common_artist).distinct()

    return recommended_songs

def recommend_songs_by_playlist_genre(user):
    playlists = Playlist.objects.filter(user=user)
    genre_counter = Counter()
    for playlist in playlists:
        for song in playlist.songs.all():
            genre_counter[song.genre] += 1
    most_common_genre = genre_counter.most_common(1)
    if most_common_genre:
        most_common_genre = most_common_genre[0][0]
    recommended_songs = Song.objects.filter(genre=most_common_genre).distinct()
    return recommended_songs

class SongListView(ListView):
    model = Song
    template_name = 'song_listing.html'
    context_object_name = 'songs'

    def get_queryset(self):
        queryset = Song.objects.all()
        form = SongSearchForm(self.request.GET)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            genre = form.cleaned_data.get('genre')
            artist = form.cleaned_data.get('artist')

            if title:
                queryset = queryset.filter(title__icontains=title)
            if genre:
                queryset = queryset.filter(genre__icontains=genre)
            if artist:
                queryset = queryset.filter(artist__icontains=artist)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SongSearchForm(self.request.GET)
        return context


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'playlist_creation.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_playlists')

class PlaylistsUserView(LoginRequiredMixin, TemplateView):
    template_name = 'user_playlists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_playlists'] = Playlist.objects.filter(user=user)
        context['public_playlists'] = Playlist.objects.filter(is_public=True).exclude(user=user)
        return context

class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'playlist_detail.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()
        context['songs'] = playlist.songs.all()
        return context

class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'update_playlist.html'

    def get_object(self, queryset=None):
        playlist = get_object_or_404(Playlist, pk=self.kwargs['pk'])
        if playlist.user != self.request.user:
            return HttpResponseForbidden()
        return playlist

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('playlist_detail', kwargs={'pk': self.object.pk})

class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'playlist_confirm_delete.html'
    success_url = reverse_lazy('user_playlists')

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user
        profile = UserProfile.objects.get(user=user_profile)
        context['profile'] = profile
        context['playlists'] = Playlist.objects.filter(user=self.request.user)
        context['your_public_playlists'] = Playlist.objects.filter(is_public=True, user=self.request.user)
        context['genre_recommendations'] = recommend_songs_by_genre(profile)
        context['artist_recommendations'] = recommend_songs_by_artists(user_profile)
        context['playlist_genre_recommendations'] = recommend_songs_by_playlist_genre(user_profile)
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = CustomUserProfileUpdateForm
    template_name = 'user_profile_update.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        if profile.user != self.request.user:
            return HttpResponseForbidden()
        return profile

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/registration.html"

class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"

class UserLogoutView(LogoutView):
    template_name = "registration/logout.html"

class HomePageView(TemplateView):
    template_name = "home.html"

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')



