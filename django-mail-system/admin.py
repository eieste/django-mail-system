from django.contrib import admin
from .models import MailLogSession, MailLogLine

# Register your models here.
class MailLogLineAdmin(admin.TabularInline):
    model = MailLogLine
    readonly_fields = ["type", "payload", "insert", "protocol", "timestamp"]


class MailLogSessionAdmin(admin.ModelAdmin):
    list_display = ("send_at", "uuid", "recipient_email", "sender_email")
    inlines = [MailLogLineAdmin]
    readonly_fields = ["send_at", "uuid", "recipient_email", "sender_email", "context", "email"]

admin.site.register(MailLogSession, MailLogSessionAdmin)
