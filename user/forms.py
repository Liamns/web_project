from allauth.account.forms import SignupForm, PasswordField
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.utils import set_form_field_order, build_absolute_uri
from allauth.account.utils import get_user_model, setup_user_email, user_email
from config import settings
from .models import User

class UserSignupForm(SignupForm):
    class Meta:
        model = User
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"] = PasswordField(
            label=_("Password"), autocomplete="new-password"
        )
        if settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"] = PasswordField(
                label=_("Password (again)"), autocomplete="new-password"
            )

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

    def clean(self):
        super(SignupForm, self).clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validation.
        User = get_user_model()
        dummy_user = User()
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if (
            settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("You must type the same password each time."),
                )
        return self.cleaned_data

    def save(self, request):
        if self.account_already_exists:
            # Don't create a new acount, only send an email informing the user
            # that (s)he already has one...
            self._send_account_already_exists_mail(request)
            return
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user

    def _send_account_already_exists_mail(self, request):
        signup_url = build_absolute_uri(request, reverse("account_signup"))
        password_reset_url = build_absolute_uri(
            request, reverse("account_reset_password")
        )
        email = self.cleaned_data["email"]
        context = {
            "request": request,
            "current_site": get_current_site(request),
            "email": email,
            "signup_url": signup_url,
            "password_reset_url": password_reset_url,
        }
        get_adapter(request).send_mail(
            "account/email/account_already_exists", email, context
        )