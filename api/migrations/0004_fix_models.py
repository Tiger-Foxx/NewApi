# Generated manually to fix migration issues

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_auto_20250518_0934"),  # Assure-toi que cette référence est correcte
    ]

    operations = [
        migrations.AddField(
            model_name='visiteur',
            name='date_inscription',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]