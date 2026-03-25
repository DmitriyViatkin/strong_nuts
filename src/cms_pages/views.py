from django.shortcuts import render
from wagtail.models import Page
from cms_pages.models import Page404
from django.views import View

def page_not_found(request, exception=None):
    page = Page404.objects.live().first()
    return render(request, "cms_pages/404.html", {"page": page}, status=404)

# Create your views here.
