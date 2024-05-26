from django import template

register = template.Library()

@register.filter
def timeformat(value):
    try:
        # Ensure the value is an integer
        total_seconds = int(value)
    except ValueError:
        return "Invalid time format"  # Handle the case where conversion fails

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


