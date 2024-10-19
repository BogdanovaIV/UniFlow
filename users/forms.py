from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your first name'})
    )
    second_name = forms.CharField(
        max_length=30,
        label='Second Name',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your second name'})
        )

    def save(self, request):
        # Save the user object without a username
        user = super(CustomSignupForm, self).save(request)

        # Assign email to the username field
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.second_name = self.cleaned_data['second_name']
        user.save()

        return user