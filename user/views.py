from django.contrib.auth import get_user_model, login, logout
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user.serializers import UserSerializer
from user.service import UserService, MobileVerificationService

user_model = get_user_model()


class SendOTPRequestAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        contact_number = request.data.get('contact_number')
        if contact_number is None:
            return Response({'error': "Contact number not provided"}, status=HTTP_400_BAD_REQUEST)
        status, user_status = MobileVerificationService.send_otp(contact_number)
        return Response({'status': status, 'user_status': user_status}, status=HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'status': 'User Successfully Logged Out.'}, status=HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        if request.user is not None and request.user.is_authenticated:
            return Response({'error': 'Already logged in. Kindly logout.'}, status=HTTP_400_BAD_REQUEST)
        contact_number = request.data.get('contact_number')
        verification_code = request.data.get('verification_code')
        user = user_model.objects.filter(contact_number=contact_number, is_active=True).last()
        if user is not None:
            if MobileVerificationService.verify_otp(contact_number, verification_code):
                login(request, user)
                serialized_data = self.serializer_class(user).data
                return Response(serialized_data, status=HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Verification Code'}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User Does Not Exist. Please Register before Logging In'}, status=HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        if request.user is not None and request.user.is_authenticated:
            return Response({'error': 'Already logged in. Kindly logout before registration.'}, status=400)

        contact_number = request.data.get('contact_number', None)
        verification_code = request.data.get('verification_code')
        if not MobileVerificationService.verify_otp(contact_number, verification_code):
            return Response({'error': "Invalid Verification Code"}, status=400)
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        email = request.data.get('email', None)
        user = UserService.create_user(contact_number=contact_number, first_name=first_name, last_name=last_name, email=email)
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = UserSerializer
    queryset = user_model.objects.all()

    def patch(self, request, *args, **kwargs):
        return super(UserUpdateAPIView, self).patch(request, *args, **kwargs)
