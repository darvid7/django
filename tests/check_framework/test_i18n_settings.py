from django.conf import settings
from django.core.checks.i18n_settings import (
   check_setting_language_code
)
from django.test import SimpleTestCase
from django.test.utils import override_settings


class CheckI18nSettings(SimpleTestCase):

    @override_settings(ROOT_URLCONF='check_framework.i18n_settings.valid_language_code_format_ll_only')
    def test_valid_language_code_format_ll_only(self):
        settings.LANGUAGE_CODE = "en"
        result = check_setting_language_code(None)
        self.assertEqual(len(result), 0)

    @override_settings(ROOT_URLCONF='check_framework.i18n_settings.invalid_language_code_format__ll_only')
    def test_invalid_language_code_format_ll_only(self):
        invalid_codes = ["EN", "eN"]
        for code in invalid_codes:
            settings.LANGUAGE_CODE = code
            result = check_setting_language_code(None)
            self.assertEqual(len(result), 1)
            warning = result[0]
            self.assertEqual(warning.id, 'i18n_settings.W001')
            self.assertEqual(warning.msg, (
                "LANGUAGE_CODE in settings.py is {}. It should be lower case in the form ll or ll-cc where ll is the "
                "language and cc is the country. Examples include: it, de-at, es, pt-br.".format(code)
            ))

    @override_settings(ROOT_URLCONF='check_framework.i18n_settings.valid_language_code_format_ll_cc')
    def test_valid_language_code_format_ll_cc(self):
        settings.LANGUAGE_CODE = "en-us"
        result = check_setting_language_code(None)
        self.assertEqual(len(result), 0)

    @override_settings(ROOT_URLCONF='check_framework.i18n_settings.invalid_language_code_format_cc')
    def test_invalid_language_code_format_ll_cc(self):
        invalid_codes = ["en-US", "enus", "EN-US", "en-", "en-uS", "en_us"]
        for code in invalid_codes:
            settings.LANGUAGE_CODE = code
            result = check_setting_language_code(None)
            self.assertEqual(len(result), 1)
            warning = result[0]
            self.assertEqual(warning.id, 'i18n_settings.W001')
            self.assertEqual(warning.msg, (
                "LANGUAGE_CODE in settings.py is {}. It should be lower case in the form ll or ll-cc where ll is the "
                "language and cc is the country. Examples include: it, de-at, es, pt-br.".format(code)
            ))
