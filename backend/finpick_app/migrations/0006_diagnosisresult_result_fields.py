from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0005_diagnosisresult_test_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosisresult',
            name='invest',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='diagnosisresult',
            name='level',
            field=models.CharField(default='금융 진단 완료', max_length=50),
        ),
        migrations.AlterField(
            model_name='diagnosisresult',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='diagnosisresult',
            name='summary',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='financial_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='finpick_comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='improvements',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='profile_scores',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='readiness_score',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='diagnosisresult',
            name='strengths',
            field=models.TextField(blank=True),
        ),
    ]
