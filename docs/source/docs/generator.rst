#########
Generator
#########


You can define a generator by creating a mail.
This generator can be used to generate context for a specific E-Mail type.
For example you can use your own generator to create specific links in a "Password Forgotten" Email.


If you define your own generator you can create your own method which adds a new value to the
context or updates available context values.

The MailFactory class calls the method get_context from the basic `notification.generator.generic.BasicGenerator` to fill in the context variables. If there is a content in the class Mail, that content is used. If not, the placeholder content of the class MailTemplate is used.

D.h.

Ausgangsituation
----------------

**MailTemplate:**

- name: DefaultTemplate

**MailTemplateVariable:**

- | name: header
  | default: Hi
- | name: content
  | default: Wie gehts? Alles fit?

**Mail:**

- | subject: Welcome
  | template: DefaultTemplate
  | generator: `notification.generator.generic.BasicGenerator`
  | reason: for_every_thing


The `notification.generator.generic.BasicGenerator` call all methods with the same name like the
MailTemplateVariable and overwrites the result of the function with the result of method of the MailVariable.
Like the following Example code:

.. code-block:: python

    from notification.generator.generic import BasicGenerator
    from mailsystem.models import Mail


    class BasicGenerator:

        def <NameOfEveryVariable>(self):

            result = self.get_content_of_mail_<NameOfEveryVariable>()
            if result is None:
                result = self.get_content_of_mail_template_<NameOfEveryVariable>()
           return result


    context = {}

    gen = BasicGenerator()

    context["header"] = gen.<NameOfEveryVariable>()

The context that BasicGenerator creates was

.. code-block:: json

    {
        "header": "Hi"
        "content": "Wie gehts? Alles fit?"
    }

if the following setting was added to the Mail Configuration


**MailVariable:**

- | mail_template_variable: header
  | content: Dear Sir or Madam

- | mail_template_variable: content
  | content: Welcome to......

the result of BasicGenerator was

.. code-block:: json

    {
        "header": "Dear Sir or Madam",
        "content": "Welcome to......"
    }


If nessesary you can create your own method to create adidtional context.
Your own Method must be start with `generator_` and gets the context as parameter

.. code-block:: python

    def generate_registration_link(self, ctx):
        # ctx["reference"] contains an user object
        # do magic returns for example a string
        link = ctx["reference"].do_magic()
        return {"registration_link": link}


Your own generator should be Inherith from BasicGenerator
