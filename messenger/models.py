from django.db import models
from django.contrib.auth import get_user_model

from core.models import CommonInfo


class Channel(CommonInfo):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ChannelMember(CommonInfo):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    member = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.channel.name}-{self.member}"


class ChannelMessage(CommonInfo):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    message = models.TextField()

    def __str__(self):
        return f"{self.channel.name} - {self.sender.name}"
