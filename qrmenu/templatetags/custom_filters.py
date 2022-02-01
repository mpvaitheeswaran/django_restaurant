from datetime import datetime
from django import template
from django.utils import timezone
register = template.Library()

@register.filter()
def mul(value,arg):
    return value*arg

@register.filter()
def available_time(st,et):
    if st and et:
        if st<=datetime.time(timezone.localtime(timezone.now())) and et>=datetime.time(timezone.localtime(timezone.now())):
            return True
        else:
            return False
    return None