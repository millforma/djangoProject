from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.utils.translation import gettext_lazy as _




class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"] = forms.EmailField(
            required=True,
            widget=forms.TextInput(attrs={"placeholder": _("E-mail")}),
        )
        self.fields["first_name"] = forms.CharField(
            max_length=200,
            widget=widgets.TextInput(
                attrs={"placeholder": _("First name - (ex. John)"), }
            ),
        )
        self.fields["last_name"] = forms.CharField(
            max_length=150,
            widget=forms.TextInput(
                attrs={"placeholder": _("Last name - (ex. Walker)"), }
            ),
        )
        self.fields["username"] = forms.CharField(
            max_length=30,
            widget=forms.TextInput(
                attrs={"placeholder": _("Choose a username - (ex. Joe19)"), }
            ),
        )
        self.fields["password1"] = forms.CharField(
            max_length=16,
            widget=forms.PasswordInput(
                attrs={"placeholder": _("Password from numbers and letters of the Latin alphabet"), }
            ),
        )
        self.fields["password2"] = forms.CharField(
            max_length=16,
            widget=forms.PasswordInput(
                attrs={"placeholder": _("Password confirmation"), }
            ),
        )

