import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finpick_app', '0007_roadmaptemplate_roadmapmission_usermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('deposit', '예금'), ('saving', '적금')], max_length=20)),
                ('disclosure_month', models.CharField(blank=True, max_length=6)),
                ('financial_company_code', models.CharField(max_length=20)),
                ('financial_company_name', models.CharField(max_length=100)),
                ('product_code', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=200)),
                ('join_way', models.TextField(blank=True)),
                ('maturity_interest', models.TextField(blank=True)),
                ('special_condition', models.TextField(blank=True)),
                ('join_deny', models.CharField(blank=True, max_length=50)),
                ('join_member', models.TextField(blank=True)),
                ('etc_note', models.TextField(blank=True)),
                ('max_limit', models.BigIntegerField(blank=True, null=True)),
                ('raw_data', models.JSONField(blank=True, default=dict)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['financial_company_name', 'product_name'],
                'unique_together': {('product_type', 'financial_company_code', 'product_code')},
            },
        ),
        migrations.CreateModel(
            name='DepositOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_rate_type', models.CharField(blank=True, max_length=20)),
                ('interest_rate_type_name', models.CharField(blank=True, max_length=50)),
                ('saving_term', models.PositiveIntegerField(blank=True, null=True)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('max_interest_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('reserve_type', models.CharField(blank=True, max_length=20)),
                ('reserve_type_name', models.CharField(blank=True, max_length=50)),
                ('raw_data', models.JSONField(blank=True, default=dict)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='finpick_app.depositproduct')),
            ],
            options={
                'ordering': ['saving_term', 'interest_rate_type_name'],
                'unique_together': {('product', 'saving_term', 'interest_rate_type', 'reserve_type')},
            },
        ),
    ]
