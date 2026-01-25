from django import template

register = template.Library()


@register.simple_tag
def localized(obj, attr, lang):
    """Return localized field: attr_lang or attr. For 'tr' uses base attr."""
    if not obj:
        return ''
    if lang == 'tr':
        return getattr(obj, attr, '') or ''
    val = getattr(obj, f'{attr}_{lang}', None)
    return (val or '').strip() or (getattr(obj, attr, '') or '')
