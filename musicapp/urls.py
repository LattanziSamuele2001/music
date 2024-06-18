from django.urls import path
from .views import (SongListView, PlaylistCreateView, PlaylistUpdateView,
                    UserProfileView, SignUpView, UserLoginView,
                    PlaylistDeleteView,PlaylistsUserView, UserProfileUpdateView,
                    PlaylistDetailView, HomePageView, logout_view)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('song_listing', SongListView.as_view(), name='song_listing'),
    path('playlist/new/', PlaylistCreateView.as_view(), name='playlist_creation'),
    path('playlist/<int:pk>/edit/', PlaylistUpdateView.as_view(), name='update_playlist'),
    path('playlist/<int:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlists/', PlaylistsUserView.as_view(), name='user_playlists'),
    path('playlist/<int:pk>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('register/', SignUpView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]