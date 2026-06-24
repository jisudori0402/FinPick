from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0011_userfavoritedepositproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password_changed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
