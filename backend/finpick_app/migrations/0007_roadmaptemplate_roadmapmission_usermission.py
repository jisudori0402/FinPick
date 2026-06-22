import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0006_diagnosisresult_result_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadmapTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_code', models.CharField(max_length=50)),
                ('level', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('type_code', 'level')},
            },
        ),
        migrations.CreateModel(
            name='RoadmapMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission_title', models.CharField(max_length=100)),
                ('mission_description', models.TextField(blank=True)),
                ('category', models.CharField(blank=True, max_length=50)),
                ('order', models.PositiveIntegerField()),
                ('roadmap_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missions', to='finpick_app.roadmaptemplate')),
            ],
            options={
                'ordering': ['roadmap_template__order', 'order'],
                'unique_together': {('roadmap_template', 'mission_title')},
            },
        ),
        migrations.CreateModel(
            name='UserMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_missions', to='finpick_app.roadmapmission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_missions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'mission')},
            },
        ),
    ]
