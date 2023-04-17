# Generated by Django 4.2 on 2023-04-15 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_bookinstance_borrower"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookinstance",
            options={
                "ordering": ["due_back"],
                "permissions": (("can_mark_returned", "Set book as returned"),),
            },
        ),
    ]
