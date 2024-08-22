# Generated by Django 5.1 on 2024-08-21 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='discountPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imageUrls',
            field=models.TextField(),
        ),
    ]
