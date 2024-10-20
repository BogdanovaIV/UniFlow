from django.contrib.auth import login
from django.shortcuts import redirect
from allauth.account.views import LoginView

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.user
        login(self.request, user)

        # Redirect based on the user's group
        if user.groups.filter(name='Student').exists():
            # Replace with your student dashboard URL name
            return redirect('student_dashboard')
        else:
            return redirect('home')  # Default redirect