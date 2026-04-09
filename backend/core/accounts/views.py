from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from .models import OTPVerification, User
from .services import SmsService

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            SmsService.send_otp(phone_number)
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp_code = serializer.validated_data['otp']

            # Check latest OTP for this phone
            otp_record = OTPVerification.objects.filter(
                phone_number=phone_number, 
                otp=otp_code, 
                is_verified=False
            ).last()

            if otp_record and not otp_record.is_expired():
                otp_record.is_verified = True
                otp_record.save()

                # Get or Create User
                user, created = User.objects.get_or_create(phone_number=phone_number)
                user.is_verified = True
                user.save()

                # Generate Auth Token for the session
                token, _ = Token.objects.get_or_create(user=user)

                # Inside VerifyOTPView...

            # Inside VerifyOTPView...
                return Response({
                       "message": "OTP verified successfully",
                       "token": token.key,
                       "is_staff": user.is_staff,  # Add this line
                       "is_new_user": created
                    }, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
