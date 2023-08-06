from requests.exceptions import RequestException


class PyPayStackError(RequestException):
    """ Base error for the PayStack gateway """


class AuthorizationError(PyPayStackError):
    """ Access to the gateway was not authorized """


class ApiKeyError(PyPayStackError):
    """ Merchant key was not valid """


class InvalidDataError(PyPayStackError, ValueError):
    """ Data to or from gateway was malformed or invalid """

