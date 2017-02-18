# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
def fill_the_table(apps, schema_editor):
    test_names = apps.get_model("test_data", "InitialNames")
    with open('/home/thavr/Dropbox/ws/hk/names.txt', 'r') as input_file:
        current_names = input_file.readlines()
    input_file.close()
    current_names = [x.strip('\n') for x in current_names]
    for this_name in current_names:
        names = this_name.split(" ")
        new_name=test_names(first_name=names[0], last_name=names[1])
        new_name.save()
    


class Migration(migrations.Migration):

    dependencies = [
        ('test_data', '0001_initial'),
    ]

    operations = [
                  migrations.RunPython(fill_the_table),
    ]
