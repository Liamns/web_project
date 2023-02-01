# 이름, 별명 자동짓기
from django.utils.http import url_has_allowed_host_and_scheme
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from allauth.account.utils import user_email, user_field
import random, string
from django.urls.base import reverse

class SocialUserSignUp(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        email = data.get("email")
        name = data.get("name")
        nickname = data.get("nickname")
        user = sociallogin.user
        user_email(user, valid_email_or_none(email) or "")
        user_field(user, "name", name or "".join(random.choices(string.ascii_letters, k=5)))
        user_field(user, "nickname", nickname or "".join(random.choices(string.ascii_letters, k=7)))

        return user

    def get_signup_form_initial_data(self, sociallogin):
        user = sociallogin.user
        initial = {
            "email": user_email(user) or "",
            "name": user_field(user, "name") or "".join(random.choices(string.ascii_letters, k=5)),
            "nickname": user_field(user, "nickname") or "".join(random.choices(string.ascii_letters, k=7))
        }
        return initial

    def is_safe_url(self, url):
        allowed_hosts = ['127.0.0.1:8000', 'localhost:8000']
        return url_has_allowed_host_and_scheme(url, allowed_hosts)

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        assert request.user.is_authenticated
        url = reverse("socialaccount_connections")
        return url
# 이름, 별명 자동짓기