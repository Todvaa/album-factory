from rest_framework_simplejwt.authentication import JWTAuthentication

from common.models import Studio, Order

NAMESPACE_ATTRIBUTE = 'namespace'
NAMESPACE_STUDIO = 'studio'
NAMESPACE_CUSTOMER = 'customer'


class MultiJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        self.user_model = None
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        if NAMESPACE_ATTRIBUTE not in validated_token:
            return None
        if validated_token[NAMESPACE_ATTRIBUTE] == NAMESPACE_CUSTOMER and NAMESPACE_CUSTOMER in request.path:
            self.user_model = Order
        elif validated_token[NAMESPACE_ATTRIBUTE] == NAMESPACE_STUDIO and NAMESPACE_STUDIO in request.path:
            self.user_model = Studio
        else:
            return None
        return self.get_user(validated_token), validated_token
