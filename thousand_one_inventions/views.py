from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.utils.translation import gettext_lazy as _

from thousand_one_inventions.forms.address_form import AddressForm
from thousand_one_inventions.forms.register_form import RegisterForm
from thousand_one_inventions.models.address import EntityAddress


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm

    def get_success_url(self):
        return reverse("home")

    def form_invalid(self, form):

        # Taken from Django source code:
        """ If the form is invalid, render the invalid form. """
        return self.render_to_response(
            self.get_context_data(
                form=form)
        )

    def form_valid(self, form):
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password_1 = form.cleaned_data["password1"]
            # hack to make a fake username
            # username = email.replace("@", "_at_")
            # remove accents:
            # username = unidecode.unidecode(username)
            # replace special chars by '_':
            # username.translate(
            #    {ord(c): "_" for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=+"}
            # )
            username = form.cleaned_data["username"]


            if User.objects.filter(email=email).exists():
                form.add_error("email", _("Email already used, consider login"))
                return self.form_invalid(form)

            try:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password_1,
                )  # Person is automatically created (cf signal in person.py)


                user.save()

            except IntegrityError:
                form.add_error("username", _("Username already taken"))
                return self.form_invalid(form)

            login(self.request, user)

            return redirect('profile')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My profile"

        user = self.request.user

        context["profile_form"] = RegisterForm(
            initial={
                "first_name": _(user.first_name),
                "last_name": _(user.last_name),
                "username": _(user.username),
                "email": _(user.email),
            }
        )

        context["address_form"] = AddressForm(
            initial=[
                {
                    "type": e_a.address_type.name,
                    "details": _(e_a.address.details),
                }
                for e_a in EntityAddress.objects.filter(
                    entity=self.request.user
                )
            ],
        )

        return context

    def post(self, request, *args, **kwargs):
        _p = request.POST
        _r = request.FILES
        profile_form = RegisterForm(_p,)
        profile_form.is_valid()

        return self.form_valid(profile_form)

    @staticmethod
    def get_success_url():
        return reverse("profile")

    def form_invalid(
            self, profile_form
    ):
        # Taken from Django source code:
        """ If the form is invalid, render the invalid form. """
        return self.render_to_response(
            self.get_context_data(
                profile_form=profile_form,
            )
        )

    def form_valid(
            self, profile_form
    ):
        user = self.request.user
        if profile_form.is_valid():
            user.username = profile_form.cleaned_data["username"]
            user.first_name = profile_form.cleaned_data["first_name"]
            user.last_name = profile_form.cleaned_data["last_name"]
            user.email = profile_form.cleaned_data["email"]
            user.save()



        return HttpResponseRedirect(self.get_success_url())