# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessDataChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pasword_change', models.BooleanField(default=False)),
                ('email_change', models.BooleanField(default=False)),
                ('change_date', models.DateTimeField()),
                ('password_verification_result', models.CharField(max_length=10)),
                ('user_impacted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Users')),
            ],
        ),
        migrations.CreateModel(
            name='AuditEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField()),
                ('transaction', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('confirmation', models.CharField(blank=True, default=None, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuditEventTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PreferencesChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_changed', models.CharField(max_length=20)),
                ('old_value', models.CharField(max_length=255)),
                ('new_value', models.CharField(max_length=255)),
                ('audit_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.AuditEvent')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_changed', models.CharField(max_length=50)),
                ('old_value', models.CharField(max_length=255)),
                ('new_value', models.CharField(max_length=255)),
                ('audit_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.AuditEvent')),
            ],
        ),
        migrations.CreateModel(
            name='UserChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_changed', models.CharField(max_length=20)),
                ('old_value', models.CharField(max_length=255)),
                ('new_value', models.CharField(max_length=255)),
                ('audit_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.AuditEvent')),
            ],
        ),
        migrations.AddField(
            model_name='auditevent',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.AuditEventTypes'),
        ),
        migrations.AddField(
            model_name='auditevent',
            name='user_impacted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='victim', to='budget.Users'),
        ),
        migrations.AddField(
            model_name='auditevent',
            name='user_initiated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiator', to='budget.Users'),
        ),
    ]