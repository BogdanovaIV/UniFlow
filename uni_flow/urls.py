"""
URL configuration for uni_flow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler403, handler404, handler500
from django.shortcuts import render
from django.urls import path, include


def custom_permission_denied_view(request, exception):
    """
    Custom view to handle permission denied errors (HTTP 403).

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception raised when permission is denied.

    Returns:
        HttpResponse: A rendered 403.html template with a 403 status code.
    """
    return render(request, '403.html', status=403)


handler403 = custom_permission_denied_view


def custom_page_not_found(request, exception):
    """
    Custom view to handle the page is not found (HTTP 404).

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception raised when the page is not found.

    Returns:
        HttpResponse: A rendered 404.html template with a 404 status code.
    """
    return render(request, '404.html', status=404)


handler404 = custom_page_not_found


def custom_page_internal_server_error(request):
    """
    Custom view to handle the page gets 'Internal Server Error' (HTTP 500).

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered 500.html template with a 500 status code.
    """
    return render(request, '500.html', status=500)


handler500 = custom_page_internal_server_error

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('student/', include('student_dashboard.urls')),
    path('tutor/', include('tutor_dashboard.urls')),
    path('', include("main.urls"), name="main-urls"),
    path('', include("users.urls"), name="users-urls"),
]
