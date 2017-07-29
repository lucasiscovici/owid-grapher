# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 04:13
from __future__ import unicode_literals
from django.db import migrations, models, transaction
import json

def selectedKeysRedesign(apps, schema_editor):
    Chart = apps.get_model('grapher_admin', 'Chart')
    with transaction.atomic():
        for chart in Chart.objects.all():
            config = json.loads(chart.config)
            
            if not 'selected-countries' in config:
                continue
                
            mainDimensions = [dim for dim in config['chart-dimensions'] if dim['property'] == 'y']

            selection = []

            for entity in config['selected-countries']:
                for i, dim in enumerate(mainDimensions):
                    sel = { 'entityId': int(entity['id']), 'index': i }
                    if 'color' in entity:
                        sel['color'] = entity['color']
                    selection.append(sel)

            print(config['selected-countries'])
            print(selection)
            print()

            config['selection'] = selection
            del config['selected-countries']

            chart.config = json.dumps(config)
            chart.save()

class Migration(migrations.Migration):
    dependencies = [
        ('grapher_admin', '0004_axis_config_cleanup'),
    ]
    operations = [
        migrations.RunPython(selectedKeysRedesign),
    ]