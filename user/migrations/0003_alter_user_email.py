# Generated by Django 4.0.6 on 2022-07-20 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_rename_user_id_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=20, unique=True, verbose_name="사용자 이메일"),
        ),
    ]