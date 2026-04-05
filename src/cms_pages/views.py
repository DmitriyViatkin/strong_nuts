from django.shortcuts import render
from django.http import JsonResponse
from cities_light.models import Region
from cms_pages.models import Page404


def page_not_found(request, exception=None):
    page = Page404.objects.live().first()
    return render(request, "cms_pages/404.html", {"page": page}, status=404)


def regions_api(request):
    country_id = request.GET.get('country')
    if not country_id:
        return JsonResponse([], safe=False)
    regions = Region.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(regions), safe=False)