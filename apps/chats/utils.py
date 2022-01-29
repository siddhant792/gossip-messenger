from rest_framework.authtoken.models import Token


def autheticate_socket_user(headers):
    if b'authorization' in headers:
        try:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Token':
                token = Token.objects.get(key=token_key)
                return token.user
        except Token.DoesNotExist:
            return None
    return None
