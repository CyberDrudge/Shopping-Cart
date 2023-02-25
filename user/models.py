import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save

from user.constants import MOBILE_CODE_VALID_FOR_MINS, MOBILE_VERIFICATION_CODE_LENGTH
from user.utils import CodeGenerator


class User(AbstractUser):
    contact_number = models.CharField(max_length=16, db_index=True)
    email = models.EmailField(blank=True, null=True)
    is_blacklisted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.username is None or len(self.username) == 0:
            self.username = str(uuid.uuid4().hex)[:32]

        self.full_name = self.first_name + " " + self.last_name
        return super(User, self).save(*args, **kwargs)


class MobileVerificationCode(models.Model):
    code = models.CharField(max_length=10)
    valid_till = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=16, db_index=True)
    is_active = models.BooleanField(default=True)
    intent = models.CharField(max_length=10)

    def invalidate_old_codes(self):
        MobileVerificationCode.objects.filter(
            contact_number=self.contact_number, valid_till__gte=datetime.now()
        ).update(is_active=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def send(self):
        """
        Send OTP
        """
        pass


def pre_save_mobile_verification_code(sender, instance, *args, **kwargs):
    if instance.id is None:
        last_hour_date_time = datetime.now() - timedelta(minutes=55)
        existing_otp = MobileVerificationCode.objects.filter(
            contact_number=instance.contact_number, intent=instance.intent,
            valid_till__gt=last_hour_date_time
        ).first()
        instance.code = existing_otp.code if existing_otp else str(CodeGenerator().code(size=MOBILE_VERIFICATION_CODE_LENGTH))
        instance.valid_till = datetime.now() + timedelta(minutes=MOBILE_CODE_VALID_FOR_MINS)


pre_save.connect(pre_save_mobile_verification_code, sender=MobileVerificationCode)
