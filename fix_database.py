import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoxAPI.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from django.db import connection

def fix_content_types():
    """
    Supprime les content types de l'app 'api' et renomme ceux de 'FoxApp' vers 'api'
    """
    # Afficher les content types avant la mise à jour
    print("Content types avant mise à jour:")
    for ct in ContentType.objects.all():
        print(f"App: {ct.app_label}, Model: {ct.model}")
    
    # 1. Supprimer les ContentType api qui font doublon
    print("\nSuppression des content types de 'api'...")
    ContentType.objects.filter(app_label='api').delete()
    
    # 2. Mise à jour des content types FoxApp vers api
    updated_count = 0
    for ct in ContentType.objects.filter(app_label='FoxApp'):
        print(f"Mise à jour de {ct.app_label}.{ct.model} vers api.{ct.model}")
        ct.app_label = 'api'
        ct.save()
        updated_count += 1
    
    print(f"\n{updated_count} content type(s) mis à jour.")

    # Afficher les content types après la mise à jour
    print("\nContent types après mise à jour:")
    for ct in ContentType.objects.all():
        print(f"App: {ct.app_label}, Model: {ct.model}")

def update_auth_permissions():
    """
    Met à jour les permissions dans auth_permission
    """
    with connection.cursor() as cursor:
        # Vérifie si les permissions FoxApp existent
        cursor.execute("SELECT COUNT(*) FROM auth_permission WHERE content_type_id IN (SELECT id FROM django_content_type WHERE app_label='FoxApp')")
        result = cursor.fetchone()
        count = result[0] if result else 0
        
        if count > 0:
            print(f"Mise à jour de {count} permission(s) pour FoxApp")
            
            # Met à jour les permissions pour pointer vers les nouveaux content types
            cursor.execute("""
                UPDATE auth_permission
                SET content_type_id = (
                    SELECT ct_api.id
                    FROM django_content_type ct_api
                    JOIN django_content_type ct_foxapp ON ct_api.model = ct_foxapp.model
                    WHERE ct_api.app_label = 'api'
                    AND ct_foxapp.app_label = 'FoxApp'
                    AND ct_foxapp.id = auth_permission.content_type_id
                )
                WHERE content_type_id IN (
                    SELECT id FROM django_content_type WHERE app_label='FoxApp'
                )
            """)
            
            print("Permissions mises à jour avec succès")
        else:
            print("Aucune permission FoxApp à mettre à jour")

def update_models_tables():
    """
    Met à jour les modèles pour pointer vers les bonnes tables
    """
    print("\nMise à jour des modèles pour pointer vers les tables FoxApp...")
    print("Pour faire cette étape, tu dois modifier ton fichier models.py comme indiqué dans la documentation.")
    print("Assure-toi d'ajouter la classe Meta avec db_table pour chaque modèle.")

def main():
    print("Début de la correction de la base de données...")
    
    # 1. Mettre à jour les content types
    fix_content_types()
    
    # 2. Mettre à jour les permissions
    update_auth_permissions()
    
    # 3. Indiquer comment mettre à jour les modèles
    update_models_tables()
    
    print("\nBase de données partiellement corrigée.")
    print("ÉTAPE SUIVANTE REQUISE: Modifie ton fichier api/models.py pour spécifier les noms de tables.")
    print("Exemple pour chaque modèle:")
    print("class Meta:")
    print("    db_table = 'FoxApp_nomdumodele'")

if __name__ == "__main__":
    main()