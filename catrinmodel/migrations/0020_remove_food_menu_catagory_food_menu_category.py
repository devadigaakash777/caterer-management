# Generated by Django 5.0.7 on 2025-05-14 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catrinmodel', '0019_remove_menucategorydetails_dessert_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='menu_catagory',
        ),
        migrations.AddField(
            model_name='food',
            name='menu_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='catrinmodel.menucategory'),
        ),
    ]
