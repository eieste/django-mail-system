from django.contrib import admin

from .models import *


# Register your models here.
class MailLogLineAdmin(admin.TabularInline):
    model = MailLogLine
    readonly_fields = ["type", "payload", "insert", "protocol", "timestamp"]


class MailLogSessionAdmin(admin.ModelAdmin):
    list_display = ("send_at", "uuid", "recipient_email", "sender_email")
    inlines = [MailLogLineAdmin]
    readonly_fields = ["send_at", "uuid", "recipient_email", "sender_email", "context", "email"]


admin.site.register(MailLogSession, MailLogSessionAdmin)


class MailTemplateVariableAdmin(admin.TabularInline):
    model = MailTemplateVariable
    extra = 1


class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "html_file")
    inlines = [MailTemplateVariableAdmin]


admin.site.register(MailTemplate, MailTemplateAdmin)


class MailVariableAdmin(admin.TabularInline):
    model = MailVariable
    extra = 1


class MailAdmin(admin.ModelAdmin):
    list_display = ("subject", "reason")
    inlines = [MailVariableAdmin]

admin.site.register(Mail, MailAdmin)
