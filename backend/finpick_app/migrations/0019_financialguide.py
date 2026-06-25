# Generated for FinPick RAG financial guides.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0018_searchkeywordtrend'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('keywords', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['category', 'title'],
                'unique_together': {('category', 'title')},
            },
        ),
    ]

