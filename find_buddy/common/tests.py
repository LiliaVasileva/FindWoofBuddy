from django.core.exceptions import ValidationError
from django.test import TestCase

from find_buddy.common.validators import validate_only_letters


class ValidateOnlyLettersTest(TestCase):
    def test_when_there_is_not_only_letters_expect_to_raise_ValidationError(self):
        value = 'ysb73983#@32332'
        with self.assertRaises(ValidationError) as context:
            validate_only_letters(value)

    def test_when_there_is_only_letters_expect_to_do_nothing(self):
        value = 'Test'
        self.assertEqual(None, validate_only_letters(value))
