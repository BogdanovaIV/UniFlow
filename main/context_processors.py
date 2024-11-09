from datetime import datetime


def current_year(request):
    """
    Returns the current year as a context variable.

    Args:
        request: The HTTP request object (not used in this function but
        required by the view signature).

    Returns:
        dict: A dictionary containing the key 'current_year' with the current
        year as its value.
    """
    return {
        'current_year': datetime.now().year
    }
