# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessDataChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pasword_change', models.BooleanField(default=False)),
                ('email_change', models.BooleanField(default=False)),
                ('change_date', models.DateTimeField()),
                ('password_verification_result', models.CharField(max_length=10)),
                ('user_impacted', models.ForeignKey(to='budget.Users')),
            ],
        ),
    ]
