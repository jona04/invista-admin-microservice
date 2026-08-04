from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import datetime, jwt
from core.models import User, UserToken
from app import settings

JWT_COOKIE_NAME = 'jwt'


def set_jwt_cookie(response, token):
    """Attach the authentication token to a response as a hardened cookie.

    Centralised so that issuing and clearing the cookie always agree on the
    attributes. If they diverge, the browser refuses to overwrite or remove the
    cookie and logout silently stops working.

    Args:
        response: The response object that will carry the cookie.
        token: The encoded JWT to store.
    """
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
    )


def clear_jwt_cookie(response):
    """Remove the authentication cookie from the client.

    Uses set_cookie with an immediate expiry instead of delete_cookie because
    the latter cannot send the Secure flag for a cookie without a __Secure-
    prefix. A SameSite=None cookie sent without Secure is rejected outright by
    the browser, so the removal would never take effect.

    Args:
        response: The response object that will carry the expiry.
    """
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value='',
        max_age=0,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
    )


class JWTAuthentication(BaseAuthentication):
    """DRF authentication backend reading a JWT from a cookie.

    Validity depends on two independent checks: the signature must verify
    against SECRET_KEY, and a matching unexpired row must exist in UserToken.
    The second one is what makes revocation possible — deleting the row ends
    the session immediately, without waiting for the token to expire.
    """

    def authenticate(self, request):
        """Resolve the request's user from the authentication cookie.

        Args:
            request: The incoming request.

        Returns:
            A (user, auth) tuple when the cookie holds a valid token, or None
            when no cookie is present, which DRF treats as anonymous.

        Raises:
            AuthenticationFailed: The token is expired, carries the wrong
                scope, points at a missing user, or has been revoked.
        """
        is_financeiro = 'api/financeiro' in request.path

        token = request.COOKIES.get(JWT_COOKIE_NAME)

        if not token:
            return None
        
        payload = JWTAuthentication.get_payload(token)
        
        # if (is_financeiro and payload['scope'] != 'financeiro') or ((not is_financeiro) and payload['scope'] != 'admin'):
        if not is_financeiro and payload['scope'] == 'financeiro':
            raise exceptions.AuthenticationFailed('Escopo invalido')

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('usuario nao encontrado')
        
        if not UserToken.objects.filter(user_id=user.id, 
                                        token=token, 
                                        expired_at__gt=datetime.datetime.utcnow()
                                        ).exists():
            raise exceptions.AuthenticationFailed('Nao autenticado')

        return (user, None)


    @staticmethod
    def get_payload(token):
        """Decode a token and return its payload.

        Args:
            token: The encoded JWT.

        Returns:
            The decoded payload dictionary.

        Raises:
            AuthenticationFailed: The token has expired.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('nao autenticado')

        return payload

    @staticmethod
    def generate_jwt(id, scope):
        """Issue a signed token for a user, valid for one day.

        Args:
            id: Primary key of the authenticated user.
            scope: Access scope carried in the payload.

        Returns:
            The encoded JWT as a string.
        """
        payload = {
            'user_id': id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    