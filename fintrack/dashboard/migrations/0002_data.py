# Generated by Django 4.2.2 on 2023-10-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(max_length=100)),
                ('account', models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card'), ('UPI', 'UPI'), ('Account', 'Account')], max_length=20)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('category_type', models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense')], max_length=10)),
            ],
        ),
    ]
