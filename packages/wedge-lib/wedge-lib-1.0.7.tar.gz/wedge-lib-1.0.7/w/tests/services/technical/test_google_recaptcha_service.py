import pytest

from w.services.technical.google_recaptcha_service import RecaptchaService
from w.tests.helpers import request_test_helper
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestRecaptchaService(TestCaseMixin):
    """
    verify_token
    """

    def test_verify_token_with_bad_token_raise_runtime_error(self):
        """ Ensure method raise RuntimeError """
        response = request_test_helper.get_response(
            json_file=self.get_datasets_dir("recaptcha/bad_token.json")
        )

        match = "Service Recaptcha error: invalid-input-response mocked"
        with request_test_helper.mock_request(response, method="post"):
            with pytest.raises(RuntimeError, match=match):
                RecaptchaService.verify_token("bad_token")

    def test_verify_token_with_good_token_return_score(self):
        """ Ensure method raise RuntimeError """
        response = {
            "json_file": self.get_datasets_dir("recaptcha/good_token.json"),
        }

        with request_test_helper.request_success(response, method="post"):
            assert 0.9 == RecaptchaService.verify_token("good_token")
