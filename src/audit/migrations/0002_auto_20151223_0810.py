# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 07:10
from __future__ import unicode_literals

from django.db import migrations

def fill_the_table(apps, schema_editor):
    audit_type = apps.get_model("audit", "AuditEventTypes")
    types_of_events= ["user_created", "user_edited", "user_deleted", \
                    "transaction_created", "transaction_edited", \
                    "transaction_deleted", "private_transaction_created", \
                    "private_transaction_edited", \
                    "private_transaction_deleted", "family_confirmation_sent", \
                    "family_confirmed", "email_confiration_sent", \
                    "email_confirmed", "email_confirmation_expired", \
                    "family_confirmation_expired", "site_preferences_edited", \
                    "unknown_event"]
    for this_event in types_of_events:
        new_event=audit_type(event_type=this_event)
        new_event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
                  migrations.RunPython(fill_the_table),
    ]
