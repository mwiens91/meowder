"""Views for common error statuses."""

from django.shortcuts import render


def handler403(request, exception, template_name="error403.html"):
    """Page for a 403 error."""
    return render(request, template_name, status=403)


def handler404(request, exception, template_name="error404.html"):
    """Page for a 404 error."""
    return render(request, template_name, status=404)


def handler500(request, exception, template_name="error500.html"):
    """Page for a 500 error."""
    return render(request, template_name, status=500)
