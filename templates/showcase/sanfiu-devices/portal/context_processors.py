from .models import Device

def navigation(request):
    return {"device_categories":Device.CATEGORY_CHOICES}
