from api.authentication import NAMESPACE_ATTRIBUTE, NAMESPACE_CUSTOMER
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import Order
from .serializers import SignInSerializer, OrderSerializer


class CustomerSignInView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get('order_id')
        passcode = serializer.validated_data.get('passcode')

        try:
            order = Order.objects.get(
                id=order_id,
                passcode=passcode,
            )
        except Order.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')

        refresh = RefreshToken.for_user(order)
        refresh[NAMESPACE_ATTRIBUTE] = NAMESPACE_CUSTOMER
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data)


class MeView(GenericAPIView):
    def get(self, request):
        return Response(OrderSerializer(request.user).data)
