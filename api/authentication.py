from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Authentification par token avec expiration
    """
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token invalide')

        # Vérification de l'expiration du token (si configuré)
        token_lifetime = getattr(settings, 'TOKEN_EXPIRED_AFTER_SECONDS', None)
        
        if token_lifetime is not None:
            expiration_date = token.created + timedelta(seconds=token_lifetime)
            
            if expiration_date < timezone.now():
                token.delete()
                raise AuthenticationFailed('Token expiré')

        if not token.user.is_active:
            raise AuthenticationFailed('Utilisateur désactivé')

        return (token.user, token)