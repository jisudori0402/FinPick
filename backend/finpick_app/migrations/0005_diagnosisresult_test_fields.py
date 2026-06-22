from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0004_userprofile_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosisresult',
            name='asset_level',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='financial_goal',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='income_level',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='investment_style',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='loan_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='spending_style',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
