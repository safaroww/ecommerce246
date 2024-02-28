from django import template

register = template.Library()

@register.simple_tag
def get_querystring(request, key, value):
    querydict = request.GET.copy()
    querydict[key] = value
    querystring = querydict.urlencode()
    return '?' + querystring