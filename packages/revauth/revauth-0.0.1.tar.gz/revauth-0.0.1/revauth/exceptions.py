from rest_framework import exceptions


class APIError(exceptions.APIException):
    status_code = 500
    detail = None
    code = None

    def __init__(self, detail=None, code=None):
        if detail:
            self.detail = detail
        if code:
            self.code = code


class UserExistsError(APIError):
    status_code = 400
    detail = 'user is exists'
    code = 'user_exists'


class InvalidCodeError(APIError):
    status_code = 400
    detail = 'this code is invalid'
    code = 'invalid_code'


class JWTDecodError(APIError):
    status_code = 400
    detail = 'jwt decode error'
    code = 'invalid_jwt'
