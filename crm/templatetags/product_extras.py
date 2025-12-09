from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def product_url(context, product):
    request = context.get("request")
    url = product.get_absolute_url(request=request)
    print("DEBUG product_url:", product.name, "=>", url)
    return url