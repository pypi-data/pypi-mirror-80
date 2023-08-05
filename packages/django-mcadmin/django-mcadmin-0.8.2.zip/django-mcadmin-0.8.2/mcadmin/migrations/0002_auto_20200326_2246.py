# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/migrations/0001_initial.py

# Generated by Django 3.0.4 on 2020-03-26 22:46


from typing import List, Tuple, Union  # pylint: disable=W0611

import django.db.models.deletion
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mcadmin", "0001_initial"),
    ]  # type: List[Tuple[str, str]]

    operations = [
        migrations.AlterModelOptions(
            name="commandgrouppermission",
            options={
                "ordering": ["group"],
                "verbose_name": "management command group permission",
                "verbose_name_plural": "management commands groups permissions",
            },
        ),
        migrations.AlterModelOptions(
            name="commandpermission",
            options={
                "ordering": ["command"],
                "verbose_name": "management command permission",
                "verbose_name_plural": "management commands permissions",
            },
        ),
        migrations.AlterField(
            model_name="command",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commands",
                to="mcadmin.Group",
                verbose_name="group",
            ),
        ),
        migrations.AlterField(
            model_name="commandpermission",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commands_permissions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]  # type: List[Union[migrations.AlterModelOptions, migrations.AlterField]]
