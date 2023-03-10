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

from django.contrib.auth.hashers import make_password

class UserSignupForm(SignupForm):

    email =  forms.EmailField(widget=forms.TextInput(
        attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
            }
        ))
    name = forms.CharField(
        label=_("name"),
        max_length=64,
        widget=forms.TextInput(
            attrs={"placeholder": _("name"), "autocomplete": "name"}
        ),
    )
    nickname = forms.CharField(
        label=_("nickname"),
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": _("nickname"), "autocomplete": "nickname"}
        ),
    )
    birth = forms.CharField(
        label=_("birth"),
        max_length=20,
        widget=forms.TextInput(
            attrs={"placeholder": _("birth"), "autocomplete": "birth"}
        ),
    )
    address = forms.CharField(
        label=_("address"),
        max_length=128,
        widget=forms.TextInput(
            attrs={"placeholder": _("address"), "autocomplete": "address"}
        ),
    )      

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
       
    def clean(self):
        super(UserSignupForm, self).clean()
        
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            self.add_error(
                "password2",
                _("You must type the same password each time."),
            )
        return self.cleaned_data

    # def clean_email(self):
    #     value = self.cleaned_data["email"]

    #     user = User.objects.filter(email=value)
    #     if user:
    #         self.account_already_exists = True      
    #     return value

    def save(self, request):    

        # email ?????? ?????? ????????? ?????? ??? ????????? ?????? ??????
        if self.account_already_exists:           
            self._send_account_already_exists_mail(request)
            return

        email = self.cleaned_data["email"]
        password1 = self.cleaned_data["password1"]
        name = self.cleaned_data["name"]
        nickname = self.cleaned_data["nickname"]
        birth = self.cleaned_data["birth"]
        address = self.cleaned_data["address"]

        user = User(email=email, password=make_password(password1),name=name,nickname=nickname,birth=birth,address=address)
        user.save()
        # emailaddress ????????? ??????
        setup_user_email(request, user, [])
        return user

    # def _send_account_already_exists_mail(self, request):
    #     signup_url = build_absolute_uri(request, reverse("register"))
    #     # password_reset_url = build_absolute_uri(
    #     #     request, reverse("account_reset_password")
    #     # )
    #     email = self.cleaned_data["email"]
    #     context = {
    #         "request": request,
    #         "current_site": get_current_site(request),
    #         "email": email,
    #         "signup_url": signup_url,
    #         # "password_reset_url": password_reset_url,
    #     }
    #     get_adapter(request).send_mail(
    #         "user/account_already_exists", email, context
    #     )