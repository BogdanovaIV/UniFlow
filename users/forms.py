from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group

class CustomSignupForm(SignupForm):
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