# encoding:utf-8
import string
from mako.lookup import TemplateLookup
from django.template import RequestContext
from django.conf import settings
from django.template.context import Context
from django.http import HttpResponse
from django.utils.crypto import constant_time_compare, get_random_string
CSRF_SECRET_LENGTH = 32
CSRF_ALLOWED_CHARS = string.ascii_letters + string.digits


def _get_new_csrf_string():
    return get_random_string(CSRF_SECRET_LENGTH, allowed_chars=CSRF_ALLOWED_CHARS)


def _salt_cipher_secret(secret):
    salt = _get_new_csrf_string()
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in secret), (chars.index(x) for x in salt))
    cipher = ''.join(chars[(x + y) % len(chars)] for x, y in pairs)
    return salt + cipher


def _unsalt_cipher_token(token):
    salt = token[:CSRF_SECRET_LENGTH]
    token = token[CSRF_SECRET_LENGTH:]
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in token), (chars.index(x) for x in salt))
    secret = ''.join(chars[x - y] for x, y in pairs)  # Note negative values are ok
    return secret


def render_to_response(request, template, data=None):
    context_instance = RequestContext(request)
    path = settings.TEMPLATES[0]['DIRS'][0]

    lookup = TemplateLookup(
        directories=[path],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )

    mako_template = lookup.get_template(template)
    if not data:
        data = {}

    if context_instance:
        context_instance.update(data)
    else:
        context_instance = Context(data)

    result = {}

    for d in context_instance:
        result.update(d)

    result['request'] = request
    if 'CSRF_COOKIE' not in request.META:
        csrf_secret = _get_new_csrf_string()
        request.META['CSRF_COOKIE'] = _salt_cipher_secret(csrf_secret)
        result['csrf_token'] = ('<input type="hidden" name="csrfmiddlewaretoken" value={} />'.
                                format(request.META['CSRF_COOKIE']))
    else:
        csrf_secret = _unsalt_cipher_token(request.META["CSRF_COOKIE"])
        result['csrf_secret'] = csrf_secret
        result['csrf_token'] = ('<input type="hidden" name="csrfmiddlewaretoken" value={} />'
                                .format(request.META['CSRF_COOKIE']))

    return HttpResponse(mako_template.render(**result))

