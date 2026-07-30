from django import template

register = template.Library()

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f'{days}d :' if days else ''
    hours_str = f'{hours}h :' if hours else ''
    minutes_str = f'{minutes}m ' if minutes else ''

    return f'{days_str}{hours_str}{minutes_str}'

@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)
    
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
        
    return url
