from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from .models import (
    Profile, Project, Post, Visiteur, Commentaire, 
    Message, Annonce, Newsletter, Timeline, Temoignage
)

# Formulaire pour importer des emails
class ImportEmailsForm(forms.Form):
    file = forms.FileField(label='Fichier texte avec emails')

# Admin pour Visiteur avec fonctionnalité d'import
class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom')
    search_fields = ('email', 'nom')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-emails/', self.admin_site.admin_view(self.import_emails_view), name='import_emails'),
        ]
        return custom_urls + urls
    
    def import_emails_view(self, request):
        if request.method == 'POST':
            form = ImportEmailsForm(request.POST, request.FILES)
            if form.is_valid():
                file_content = request.FILES['file'].read().decode('utf-8')
                lines = file_content.strip().split('\n')
                
                # Compteurs pour les statistiques
                added_count = 0
                existing_count = 0
                invalid_count = 0
                
                for line in lines:
                    # Nettoyer l'email de tous les espaces/tabulations
                    email = line.strip()
                    
                    # S'il y a des tabulations, ne prendre que la première partie
                    if '\t' in email:
                        email = email.split('\t')[0].strip()
                    
                    if email:  # Ignorer les lignes vides
                        try:
                            # Vérifier si l'email existe déjà
                            visiteur, created = Visiteur.objects.get_or_create(email=email)
                            if created:
                                added_count += 1
                            else:
                                existing_count += 1
                        except Exception as e:
                            # Email invalide ou autre erreur
                            invalid_count += 1
                
                self.message_user(
                    request, 
                    f"Importation terminée: {added_count} nouveaux visiteurs ajoutés, "
                    f"{existing_count} visiteurs déjà existants, "
                    f"{invalid_count} emails invalides."
                )
                return redirect('admin:index')
        else:
            form = ImportEmailsForm()
        
        context = {
            'form': form,
            'title': 'Importer des emails de visiteurs',
        }
        return render(request, 'admin/import_emails.html', context)
    
    # Ajout d'un bouton d'action pour l'importation
    actions = ['redirect_to_import']
    
    def redirect_to_import(self, request, queryset):
        return redirect('admin:import_emails')
    redirect_to_import.short_description = "Importer des emails depuis un fichier"

# Admin pour Project
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'sujet', 'date')
    search_fields = ('nom', 'categorie', 'sujet')
    list_filter = ('categorie',)

# Admin pour Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date')
    search_fields = ('titre', 'categorie', 'auteur')
    list_filter = ('categorie', 'date')

# Admin pour Timeline
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('titre', 'periode', 'ordre')
    search_fields = ('titre', 'periode')
    list_editable = ('ordre',)

# Admin pour Temoignage
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'fonction')
    search_fields = ('auteur', 'fonction', 'texte')

# Admin pour Commentaire
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('post', 'visiteur', 'date')
    search_fields = ('post__titre', 'visiteur__email', 'contenu')
    list_filter = ('date',)

# Admin pour Message
class MessageAdmin(admin.ModelAdmin):
    list_display = ('visiteur', 'objet')
    search_fields = ('visiteur__email', 'objet', 'contenu')

# Admin pour Newsletter
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'subtitle', 'main_content')

# Admin pour Annonce
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('date',)
    search_fields = ('contenuP1', 'contenuConclusion', 'contenuSitation')

# Enregistrement des modèles dans l'admin
admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Visiteur, VisiteurAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Timeline, TimelineAdmin)
admin.site.register(Temoignage, TemoignageAdmin)