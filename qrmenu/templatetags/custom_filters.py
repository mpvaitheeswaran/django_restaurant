from datetime import datetime
from django import template
from django.utils import timezone

from qrmenu.models import AccountSetting,MenuCategory,MenuItem, Pack,ScanCount
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

@register.filter()
def phone(value):
    return AccountSetting.objects.get(restaurant=value).phone

@register.filter()
def total_menu(value):
    menu_count = 0
    for category in MenuCategory.objects.filter(restaurant=value):
        for menu in MenuItem.objects.filter(category=category):
            menu_count += 1 
    return menu_count

@register.filter()
def total_scan(value):
    scan_count = ScanCount.objects.filter(restaurant=value).count()
    return scan_count

@register.filter()
def pack_type(value):
    pack_id = Pack.objects.get(restaurant=value).pack_type
    if pack_id == -1:
         return 'No Pack'
    elif pack_id == 0:
        return 'Free Pack'
    elif pack_id == 1:
        return 'Monthly Pack'
    else:
        return 'Yearly Pack'

@register.filter()
def toList(value,startat=0):
    return range(startat,value+1)