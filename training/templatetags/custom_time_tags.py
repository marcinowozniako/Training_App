from datetime import date

from django import template

register = template.Library()


@register.simple_tag
def week_nb():
    return int(date.today().isocalendar()[1])


@register.simple_tag
def year_nb():
    return int(date.today().year)
