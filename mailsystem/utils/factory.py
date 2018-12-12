import importlib
import os
from collections import namedtuple

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import get_template

from mailsystem.models import Mail
from mailsystem.utils.mail import MailLogger

MailMeta = namedtuple("MailMeta", ("to", "from_email", "reply_to"))
MailMeta.__new__.__defaults__ = ("asdf@ultraapp.de", settings.EMAIL_HOST_USER, "asdf@ultraapp.de")


class MailFactory:

    @classmethod
    def get_mail_by_reason(cls, reason):
        """
        Find Mail-Object by reason
        :param reason: Reason string
        :return Mail: Mail-Object
        """
        return Mail.objects.get(reason=reason)

    @classmethod
    def trigger(cls, **kwargs):
        """
            :param reference: Object used as Reference for E-Mail rendering. eg. User Model Object
            :param mail: MailTemplate Object (Model from mailsystem)
            :param reason: String that descripe an MailTemplate
            :return:
        """
        #Extract kwargs
        reference = kwargs.pop("reference")
        mail = kwargs.pop("mail")
        reason = kwargs.pop("reason")
        meta = kwargs.pop("meta")

        # Check given Arguments
        if reason is not "" and mail is not None:
            raise ValueError("reason/mail are mutally exclusive")
        elif mail is None and reason == "":
            raise ValueError("reason/mail are mutally exclusive")

        # Convert reason_string to "MailTemplate"
        if not reason == "":
            mail = Mail.objects.get(reason=reason)

        # Load generator deposited on Mail-Object
        generator = cls.get_generator(mail)

        # Add all kwargs as context
        ctx = kwargs

        # Add reference to Context
        ctx.update({"reference": reference})

        # Update Context via Mail - Generator
        ctx.update(cls.get_context(generator(mail)))

        # Load and render html and txt emails
        html, txt = cls.render(mail, ctx)

        # Prepare for email send
        mail = EmailMultiAlternatives(subject=mail.subject,
                               from_email=meta.from_email,
                               to=meta.to,
                               body=txt)
        # Attach html body
        mail.attach_alternative(html, "text/html")

        # Log E-Mail
        with MailLogger(mail) as msg:
            msg.send()

    @classmethod
    def render(cls, mail, ctx):
        """
        Load templates and render to html and txt email content
        :param mail: Mail-Database-Object
        :param ctx: Context
        :return tupel: Tupel of html and txt template (html, txt)
        """
        html_template = get_template(os.path.join(settings.BASE_DIR, mail.template.html_file))
        mail_html_body = html_template.render(ctx)

        alternative_template = get_template(os.path.join(settings.BASE_DIR, mail.template.alternative_file))
        mail_alternative_body = alternative_template.render(ctx)

        for i in range(0, 1):
            html_template = Template(mail_html_body)
            mail_html_body = html_template.render(Context(ctx))

            alternative_template = Template(mail_alternative_body)
            mail_alternative_body = alternative_template.render(Context(ctx))

        return (mail_html_body, mail_alternative_body)


    @classmethod
    def get_context(cls, generator):
        """
        Generate Context dict use the given generator
        :param generator:
        :return:
        """
        ctx = {}
        # Itterate over all MailTemplateVariables
        # Try to resolve it via generator
        for field in generator.mail.template.mailtemplatevariable_set.all():
            ctx[field.name] = getattr(generator, field.name)()

        # Call all methods in generator that started with "generate_"
        for classmethodname in dir(generator):
            if classmethodname[:9] == "generate_":
                generate_ctx = getattr(generator, classmethodname)(ctx)
                ctx.update(generate_ctx)
        return ctx

    @classmethod
    def get_generator(cls, mail):
        """
            Import the generator from Mail Database Object
            :param mail: Mail-Database Object
            :return module: Generator Module
        """
        function_string = mail.generator
        mod_name, func_name = function_string.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        return func