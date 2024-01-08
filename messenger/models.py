from django.db import models
from core.models import CommonInfo


class Channel(CommonInfo):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ChannelUser(CommonInfo):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ChannelMessage(CommonInfo):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    sender = models.ForeignKey(ChannelUser, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.channel.name} - {self.sender.name}'
