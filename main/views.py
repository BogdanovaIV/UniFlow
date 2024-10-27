from django.shortcuts import render
import os
if os.path.isfile('env.py'):
    import env

# Create your views here.
def home(request):
    """
    Renders the Home page
    """
    return render(
        request,
        "main/home.html",
    )


def contact(request):
    """
    Renders the Contact page
    """
    return render(
        request,
        "main/contact.html",
        { "google_maps_api_key": os.environ.get("GOOGLE_MAPS_API_KEY") }
    )
