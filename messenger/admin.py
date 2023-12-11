from django.contrib import admin
from messenger.models import Channel, ChannelUser, ChannelMessage


class ChannelAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", "name", "deleted_at"]
    list_filter = ["deleted_at"]


class ChannelUserAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", "name", "deleted_at"]
    list_filter = ["deleted_at"]


class ChannelMessageAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", "channel", "sender", "message"]
    autocomplete_fields = ['channel', 'sender']


admin.site.register(Channel, ChannelAdmin)
admin.site.register(ChannelUser, ChannelUserAdmin)
admin.site.register(ChannelMessage, ChannelMessageAdmin)
