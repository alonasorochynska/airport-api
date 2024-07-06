# Generated by Django 5.0.6 on 2024-07-06 15:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airport', '0003_airplane_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='airplane',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='airplane',
            constraint=models.UniqueConstraint(fields=('name', 'rows', 'seats_in_row', 'airplane_type'), name='unique_airplane'),
        ),
        migrations.AddConstraint(
            model_name='airplanetype',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_airplane_type_name'),
        ),
        migrations.AddConstraint(
            model_name='airport',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_airport_name'),
        ),
        migrations.AddConstraint(
            model_name='crew',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name'), name='unique_crew_member'),
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(fields=('distance', 'source', 'destination'), name='unique_route'),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('flight', 'row', 'seat'), name='unique_ticket'),
        ),
    ]
