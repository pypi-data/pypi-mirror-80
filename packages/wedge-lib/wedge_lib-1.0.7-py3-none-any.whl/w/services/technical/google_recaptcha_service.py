import ast

from django.conf import settings

from w.services.abstract_service import AbstractService
from w.services.technical.request_service import RequestService


class RecaptchaService(AbstractService):
    @staticmethod
    def verify_token(recaptcha_token):
        """
        Get Recaptcha V3 score with the front token
        You have to define RECAPTCHA_SECRET_KEY in settings
        with recaptcha server api key
        """

        recaptcha_data = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": recaptcha_token,
        }

        request = RequestService.post(
            "https://www.google.com/recaptcha/api/siteverify", data=recaptcha_data
        )

        # transform request.content (str) to dict object
        result = ast.literal_eval(request.content)

        if result.get("success"):
            return result.get("score")

        raise RuntimeError(
            "Service Recaptcha error: " + ", ".join(result.get("error-codes"))
        )
