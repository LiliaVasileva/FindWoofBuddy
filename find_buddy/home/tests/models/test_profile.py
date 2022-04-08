from django.test import TestCase  # надгражда тесткасе на юниттестовете


class ProfileTest(TestCase):
    def test_profile_create_when_first_name_contains_only_letter_expect_success(self):
        pass

    def test_profile_create_when_first_name_create_digit_expect_to_fail(self):
        pass

    def test_profile_create_when_first_name_create_dollar_sign_expect_to_fail(self):
        pass

    def test_profile_full_name_when_valid_expect_correct_full_name(self):
        pass


