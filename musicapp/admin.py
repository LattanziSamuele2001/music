from django.contrib import admin
from .models import UserProfile, Song
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm


admin.site.register(UserProfile)
admin.site.register(Song)
