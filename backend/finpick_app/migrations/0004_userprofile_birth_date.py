from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0003_diagnosisresult_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
