# Generated by Django 2.1.4 on 2018-12-12 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(help_text='E-Mail Betreff', max_length=255)),
                ('generator', models.CharField(default='notification.generator.generic.BasicGenerator', max_length=255)),
                ('reason', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailLogLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField()),
                ('type', models.CharField(max_length=255)),
                ('payload', models.TextField()),
                ('insert', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailLogSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('reference', models.CharField(blank=True, max_length=255, null=True)),
                ('recipient_email', models.EmailField(max_length=255)),
                ('sender_email', models.EmailField(max_length=255)),
                ('context', models.TextField()),
                ('email', models.TextField()),
                ('send_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('html_file', models.FilePathField(max_length=500, path='mailsystem/templates/mailsystem/', recursive=True)),
                ('alternative_file', models.FilePathField(max_length=500, path='mailsystem/templates/mailsystem/', recursive=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailTemplateVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Variablen Name', max_length=255)),
                ('default', models.TextField(default='Undefined Value')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsystem.MailTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='MailVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mailsystem.Mail')),
                ('mail_template_variable', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mailsystem.MailTemplateVariable')),
            ],
        ),
        migrations.AddField(
            model_name='maillogline',
            name='protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsystem.MailLogSession'),
        ),
        migrations.AddField(
            model_name='mail',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mailsystem.MailTemplate'),
        ),
    ]
