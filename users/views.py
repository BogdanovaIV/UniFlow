from django.contrib.auth import login
from django.shortcuts import redirect
from allauth.account.views import LoginView, SignupView


class CustomAuthMixin:
    """ Mixin to handle redirection based on the user's group. """
    def redirect_based_on_group(self, user):
        """Redirects user based on group membership."""
        if user.groups.filter(name='Student').exists():
            return redirect('student:dashboard')
        elif user.groups.filter(name='Tutor').exists():
            return redirect('tutor:schedule')

        return redirect('home')  # Default redirect


class CustomLoginView(LoginView, CustomAuthMixin):
    """Custom login view that logs the user in and redirects based on group."""
    def form_valid(self, form):
        """Logs in the user and redirects based on group."""
        user = form.user
        login(self.request, user)

        # Use the helper method to handle redirection
        return self.redirect_based_on_group(user)


class CustomSignupView(SignupView, CustomAuthMixin):
    """
    Custom signup view that registers the user and redirects based on group.
    """
    def form_valid(self, form):
        """Registers, logs in the user, and redirects based on group."""
        user = form.save(self.request)
        login(self.request, user)

        # Use the helper method to handle redirection
        return self.redirect_based_on_group(user)
