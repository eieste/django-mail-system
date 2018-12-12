from django.utils.safestring import mark_safe


class BasicGenerator(object):

    def __init__(self, mail):
        self.mail = mail

    def __getattr__(self, name):

        if name in dir(self):
            return getattr(self, name)
        else:
            section_list = self.mail.mailvariable_set.filter(mail_template_variable__name=name)

            if len(section_list) >= 1:

                def wrapper(*args, **kwargs):
                    return mark_safe(section_list[0].content)

                return wrapper

            default_sections = self.mail.template.mailtemplatevariable_set.filter(name=name)
            if len(default_sections) >= 1:

                def wrapper(*args, **kwargs):
                    return mark_safe(default_sections[0].default)

                return wrapper

            raise AttributeError("Attribute {} does not exist".format(name))
