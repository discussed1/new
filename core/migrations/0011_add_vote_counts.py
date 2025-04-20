from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_payment'),  # Using the latest migration as dependency
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='upvote_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='downvote_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='upvote_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='downvote_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]