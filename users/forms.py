from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    """
    Custom signup form for handling user registration with additional fields
    for first name and last name. This form overrides the default `SignupForm`
    to automatically assign the user's email as their username and add them to
    the "Student" group upon registration.

    Attributes:
        first_name (forms.CharField): A form field for the user's first name.
        last_name (forms.CharField): A form field for the user's last name.
    """
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your first name'})
    )
    last_name = forms.CharField(
        max_length=30,
        label='Lasr Name',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your last name'})
        )

    def save(self, request):
        """
        Save the user object, assigning email as the username and adding them
        to the "Student" group.

        Args:
            request (HttpRequest): The HTTP request object containing the
            user's form data.

        Returns:
            User: The saved user object.
        """
        # Save the user object without a username
        user = super(CustomSignupForm, self).save(request)

        # Assign email to the username field
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        student_group = Group.objects.get(name='Student')
        user.groups.add(student_group)

        user.save()

        return user
