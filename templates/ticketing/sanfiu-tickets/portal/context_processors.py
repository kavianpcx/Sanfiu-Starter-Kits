from .models import Event

def navigation(request):
    return {"event_categories": Event.CATEGORY_CHOICES}
