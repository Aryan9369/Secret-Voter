import random
from .models import OTPVerification

class SmsService:
    @staticmethod
    def send_otp(phone_number):
        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Save to DB (In prod, we might hash this)
        OTPVerification.objects.create(phone_number=phone_number, otp=otp)
        
        # MOCK: Instead of calling Twilio/Firebase, we print to console
        print("\n" + "="*30)
        print(f"SMS SENT TO: {phone_number}")
        print(f"OTP CODE: {otp}")
        print("="*30 + "\n")
        
        return True