from .models import Course

def academy_navigation(request):
    return {"course_categories": Course.CATEGORY_CHOICES}
