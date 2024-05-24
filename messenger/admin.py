from django.contrib import admin
from messenger.models import Channel, ChannelMember, ChannelMessage


class ChannelAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", "name", "deleted_at"]
    list_filter = ["deleted_at"]


class ChannelMemberAdmin(admin.ModelAdmin):
    search_fields = ["id", "channel__name", "member__last_name", "member__first_name"]
    list_display = ["id", "channel", "member", "deleted_at"]
    list_filter = ["deleted_at"]


class ChannelMessageAdmin(admin.ModelAdmin):
    search_fields = ["id", "channel__name"]
    list_display = ["id", "channel", "message"]
    autocomplete_fields = ["channel"]


admin.site.register(Channel, ChannelAdmin)
admin.site.register(ChannelMember, ChannelMemberAdmin)
admin.site.register(ChannelMessage, ChannelMessageAdmin)
