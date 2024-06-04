# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile


@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    """A view to update a user's profile.

    Attributes:
    - model: The model to use for the view.
    - form_class: The form class to use for the view.
    - template_name: The name of the template for the view.
    - success_url: URL to redirect to after a successful update.

    Methods:
    - get_object: Gets the user profile object.
    - get_context_data: Gets the data context for the template.
    - form_valid: Processes the form data when validating it."""

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        """Gets the user's profile object.

        Returns:
        - User profile object."""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """
        Gets the data context for the template.

        Parameters:
        - **kwargs: Optional arguments.

        Returns:
        - The data context for the template.
        """
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["user_form"] = UserUpdateForm(
                self.request.POST, instance=self.request.user
            )
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        """
        Processes form data when validating it.

        Parameters:
        - form: valid form.

        Returns:
        - Redirect to success_url on successful profile update.
        """
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
            form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )


@method_decorator(login_required, name="dispatch")
class ProfileDetailView(DetailView):
    """
    A view for displaying a user's profile.

    Attributes:
    - model: The model to use for the view.
    - template_name: The name of the template for the view.
    - context_object_name: The name of the context variable for the profile object.

    Methods:
    - get_object: Gets the user's profile object.
    """

    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self):
        """
        Gets the user's profile object.

        Returns:
        - User profile object.
        """
        return self.request.user.profile
