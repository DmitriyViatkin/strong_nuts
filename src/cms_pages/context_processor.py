from cms_pages.models import AddressPage

def cabinet_pages (request):
    try:

        address_page = AddressPage.objects.live().first()
    except Exception:
        address_page = None

    return {
        'address_page': address_page
    }