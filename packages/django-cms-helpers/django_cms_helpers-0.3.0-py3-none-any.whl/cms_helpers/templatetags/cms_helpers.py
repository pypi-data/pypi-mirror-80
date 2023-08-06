from cms.cache import _get_cache_key
from cms.models import Page, get_cms_setting
from cms.utils.moderator import use_draft
from django import template
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import get_language


register = template.Library()

NO_EXTENSION = 'no_extension'
CMS_HELPERS_PAGE_TITLEEXTENSION_CACHE = 'CMS_HELPERS_PAGE_TITLEEXTENSION_CACHE'


def is_caching_desired(do_cache):
    if do_cache is not None:
        return do_cache
    custom_setting = getattr(settings, CMS_HELPERS_PAGE_TITLEEXTENSION_CACHE, None)
    if custom_setting is not None:
        return custom_setting
    return get_cms_setting('PLUGIN_CACHE')


@register.simple_tag(takes_context=True)
def page_titleextension(context, page_id, extension, do_cache=None):
    do_cache = is_caching_desired(do_cache=do_cache)
    request = context.get('request')
    is_draft = request and hasattr(request, 'user') and use_draft(request)

    if do_cache:
        lang = get_language()
        site_id = settings.SITE_ID
        cache_duration = get_cms_setting('CACHE_DURATIONS')['content']
        page_cache_key = _get_cache_key('page_titleextension', page_id, lang, site_id)
        cache_key = '{}_{}_{}'.format(page_cache_key, is_draft, extension)

        cached = cache.get(cache_key)
        if cached:
            if cached == NO_EXTENSION:
                return None
            return cached

    try:
        page = Page.objects.get(pk=page_id)
        if is_draft:
            page = page.get_draft_object()
        else:
            page = page.get_public_object()
    except NameError:
        raise ImportError(
            'django-cms is required when using page_titleextension tag')
    except Page.DoesNotExist:
        return None

    if not page:
        return None

    try:
        title_extension = getattr(page.get_title_obj(), extension)
    except ObjectDoesNotExist:
        if do_cache:
            cache.set(cache_key, NO_EXTENSION, timeout=cache_duration)
        return None
    else:
        if do_cache:
            cache.set(cache_key, title_extension, timeout=cache_duration)
        return title_extension
