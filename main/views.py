from django.shortcuts import render
from datetime import datetime

current_year = datetime.now().year

# Create your views here.
def home(request):
    """
    Renders the Home page
    """
    
    
    
    return render(
        request,
        "main/home.html",
        { "current_year": current_year},

    )