from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finpick_app', '0012_userprofile_password_changed_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavoriteStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('isin_code', models.CharField(blank=True, max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('market', models.CharField(blank=True, max_length=20)),
                ('base_date', models.CharField(blank=True, max_length=8)),
                ('current_price', models.BigIntegerField(default=0)),
                ('change', models.BigIntegerField(default=0)),
                ('change_rate', models.FloatField(default=0)),
                ('volume', models.BigIntegerField(default=0)),
                ('market_cap', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_stocks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
                'unique_together': {('user', 'code')},
            },
        ),
    ]
