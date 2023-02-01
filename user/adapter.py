from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        path = "/"
        return path

    def get_login_redirect_url(self, request):
        path ="/"
        return path

    def get_email_confirmation_redirect_url(self, request):
        path ="/"
        return path
