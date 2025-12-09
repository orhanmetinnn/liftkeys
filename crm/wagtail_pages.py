from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from .models import Product  # senin mevcut Product modeli

class ProductPage(Page):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wagtail_pages"
    )

    body = StreamField([
        ("text", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
        ("video", blocks.URLBlock()),
        ("feature_list", blocks.ListBlock(blocks.CharBlock(label="Özellik"))),
    ], use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("product"),
        FieldPanel("body"),
    ]