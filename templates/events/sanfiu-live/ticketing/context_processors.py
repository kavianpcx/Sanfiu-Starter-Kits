from .models import Event


def event_navigation(request):
    return {"event_categories": Event.CATEGORY_CHOICES}
