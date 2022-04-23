from datetime import date

from django import template

register = template.Library()


@register.simple_tag
def week_nb():
    """Custom tag with number of current week, required for workout list view """
    return int(date.today().isocalendar()[1])


@register.simple_tag
def year_nb():
    """Custom tag with current year, required for workout list view """
    return int(date.today().year)
