from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail_cms.blocks import VideoBannerBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, CharBlock

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail_cms.blocks import VideoBannerBlock, BenefitItemBlock, GalleryBlock


class UserAgreement(Page):

    template = 'cms_page/user_agreement.html'

    text = RichTextField(

    )



