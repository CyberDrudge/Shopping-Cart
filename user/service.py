from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.serializers import ValidationError

from user.constants import MOBILE_CODE_VALID_FOR_MINS, UserStatusChoices, UserIntentChoices
from user.models import MobileVerificationCode
from user.serializers import UserSerializer


user_model = get_user_model()


class UserService:
	@classmethod
	def get_user_status(cls, contact_number):
		user = user_model.objects.filter(contact_number=contact_number).first()
		if user:
			if user.is_blacklisted:
				status = UserStatusChoices.BLACKLISTED
			else:
				status = UserStatusChoices.RETURNING
		else:
			status = UserStatusChoices.NEW
		return status

	@classmethod
	def check_if_user_exists(cls, contact_number):
		return user_model.objects.filter(contact_number=contact_number).exists()

	@classmethod
	def create_user(cls, **kwargs):
		contact_number = kwargs.get('contact_number')
		if cls.check_if_user_exists(contact_number):
			raise ValidationError("Account Already Exists.")
		serializer = UserSerializer(data=kwargs)
		if serializer.is_valid(raise_exception=True):
			user = serializer.save()
			return user


class MobileVerificationService:
	@classmethod
	def send_otp(cls, contact_number):
		user_status = UserService.get_user_status(contact_number)
		if user_status == UserStatusChoices.RETURNING:
			intent = UserIntentChoices.LOGIN
		elif user_status == UserStatusChoices.NEW:
			intent = UserIntentChoices.REGISTER
		else:
			status = 'Mobile Code not sent'
			return status, user_status
		MobileVerificationCode.objects.create(contact_number=contact_number, intent=intent)
		status = 'Mobile Code sent'
		return status, user_status

	@classmethod
	def verify_otp(cls, contact_number, verification_code):
		return MobileVerificationCode.objects.using('default').filter(
			code=verification_code, contact_number=contact_number, is_active=True,
			valid_till__range=(timezone.now(), timezone.now() + timezone.timedelta(minutes=MOBILE_CODE_VALID_FOR_MINS))
		).exists()
