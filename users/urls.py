from django.urls import path
from .views import ProfileUpdateView, ProfileDetailView

urlpatterns = [
    path("profile_update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
]
