from django.db import models
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from cabinet.forms import AddressForm
from cabinet.models import User, Address


class AddressPage(Page):
    template = 'cms_pages/address.html'
    max_count = 1
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Зображення на сторінці'
    )
    content_panels = Page.content_panels + [
        FieldPanel('image'),
    ]

    def serve(self, request):
        user = request.user
        user.refresh_from_db()
        print("user.address:", user.address)
        print("user.address.pk:", getattr(user.address, 'pk', None))
        address = user.address  # зберігаємо в змінну
        print("address:", address)
        print("address.pk:", getattr(address, 'pk', None))
        print("address.country:", getattr(address, 'country', None))
        print("address.country.pk:",
              getattr(getattr(address, 'country', None), 'pk', None))
        form = AddressForm(request.POST or None, instance=user.address)
        print("form.initial:", form.initial)
        print("form['country'].value():", form['country'].value())
        if request.method == 'POST' and form.is_valid():
            address = form.save(commit=False)
            address.address_type = Address.TYPE_PHYSICAL
            address.save()
            User.objects.filter(pk=user.pk).update(address=address)
            return redirect(self.url)

        context = self.get_context(request)
        context['address_form'] = form
        return TemplateResponse(request, self.template, context)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return context

    class Meta:
        verbose_name = 'Сторінка адреси'