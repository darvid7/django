import re

from django.conf import settings

from . import Tags, Warning, register

LANGUAGE_LOCALE_PATTERN = re.compile(r'^[a-z]{2}(-[A-Z]{2})?$')
LANGUAGE_CODE_PATTERN = re.compile(r'^[a-z]{2}(-[a-z]{2})?$')


@register(Tags.i18n_settings)
def check_setting_language_code(app_configs, **kwargs):
    """
    Warn if language code is in the wrong format. Language codes are generally represented in lower-case with a dash
    separator.
    """
    match_result = re.match(LANGUAGE_CODE_PATTERN, settings.LANGUAGE_CODE)
    errors = []
    if not match_result:
        errors.append(Warning(
            "LANGUAGE_CODE in settings.py is {}. It should be lower case in the form ll or ll-cc where ll is the "
            "language and cc is the country. Examples include: it, de-at, es, pt-br.".format(settings.LANGUAGE_CODE),
            id="i18n_settings.W001",
        ))
    return errors
