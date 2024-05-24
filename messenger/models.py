import uuid

from utils import logging

from django.db import models
from django.contrib.auth import get_user_model

from core.models import CommonInfo


class Channel(CommonInfo):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    invite_code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def _invite_code_exists(code):
        return Channel.objects.filter(invite_code=code).exists()

    def messenger_name(self):
        return "channel_%s" % str(self.name).replace(" ", "_")

    def generate_invite_code(self):
        length = 8

        # Try to generate code 10 times
        max_attempts = 10
        for _ in range(max_attempts):
            code = uuid.uuid4().hex[:length].upper()
            if not Channel._invite_code_exists(code):
                return code

        logging.logger.critical(
            msg="Channel was not able to generate an invite code",
            extra={"channel_id": self.pk},
        )
        return ""

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)


class ChannelMember(CommonInfo):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="members"
    )
    member = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="channels"
    )

    def __str__(self):
        return f"{self.channel.name}-{self.member}"

    class Meta:
        unique_together = (("channel", "member", "deleted_at"),)


class ChannelMessage(CommonInfo):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    message = models.TextField()

    def __str__(self):
        return f"{self.channel.name} - {self.sender.username}"
