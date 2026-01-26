from django import template
from django.template.defaultfilters import truncatewords

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


@register.simple_tag
def localized_truncate(obj, attr, lang, num_words):
    """Return localized field truncated to num_words."""
    text = localized(obj, attr, lang)
    return truncatewords(text, num_words)


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    if dictionary is None:
        return None
    return dictionary.get(key)
    text = localized(obj, attr, lang)
    return truncatewords(text, num_words)
