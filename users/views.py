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
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["user_form"] = UserUpdateForm(
                self.request.POST, instance=self.request.user
            )
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
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
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile
