from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        # Assure-toi que cette référence est à ta dernière migration réussie
        ('api', '0005_alter_annonce_table_alter_commentaire_table_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE FoxApp_visiteur ADD COLUMN date_inscription DATETIME NULL;",
            "ALTER TABLE FoxApp_visiteur DROP COLUMN date_inscription;"
        ),
    ]