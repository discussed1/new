# Generated by Django 5.2 on 2025-04-20 22:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_add_vote_counts'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='community',
        ),
        migrations.AlterField(
            model_name='payment',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='donation_type',
            field=models.IntegerField(choices=[(5, 'Small ($5)'), (10, 'Medium ($10)'), (25, 'Large ($25)'), (0, 'Custom Amount')], default=5),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
