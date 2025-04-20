# Generated manually

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_avatar'),
    ]

    operations = [
        # Add MPTT fields with defaults
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='lft',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='rght',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        # Replace ForeignKey with TreeForeignKey
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.comment'),
        ),
        # Update ordering
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['tree_id', 'lft']},
        ),
    ]