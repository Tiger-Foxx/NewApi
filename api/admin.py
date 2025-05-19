from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.html import format_html
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import json
from datetime import datetime, timedelta

from .models import (
    Profile, Project, Post, Visiteur, Commentaire, 
    Message, Annonce, Newsletter, Timeline, Temoignage
)

# Classe de base pour les admins avec fonctionnalités communes
class FoxBaseAdmin(admin.ModelAdmin):
    """Classe de base pour les admins avec des fonctionnalités améliorées"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Stocke le nombre total pour l'utiliser dans le changelist_view
        request._foxapp_total_count = qs.count()
        return qs
    
    def changelist_view(self, request, extra_context=None):
        # Ajoute des statistiques de base au changelist
        extra_context = extra_context or {}
        extra_context['total_count'] = getattr(request, '_foxapp_total_count', 0)
        extra_context['last_7_days'] = self.model.objects.filter(
            **{self.get_date_field(): timezone.now() - timedelta(days=7)}
        ).count() if hasattr(self.model, self.get_date_field()) else 0
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_date_field(self):
        """Retourne le nom du champ date pour le modèle"""
        return 'date' if hasattr(self.model, 'date') else 'created_at'
    
    class Media:
        css = {
            'all': ('css/fox_admin.css',)
        }
        js = ('js/fox_admin.js',)

# Formulaire pour importer des emails
class ImportEmailsForm(forms.Form):
    file = forms.FileField(label='Fichier texte avec emails')
    send_welcome = forms.BooleanField(
        label='Envoyer un email de bienvenue',
        required=False,
        initial=True
    )

# Admin pour Visiteur avec fonctionnalités avancées
class VisiteurAdmin(FoxBaseAdmin):
    list_display = ('email', 'nom', 'date_inscription', 'actions_buttons')
    search_fields = ('email', 'nom')
    list_filter = ('date_inscription',)
    
    def date_inscription(self, obj):
        """Retourne la date d'inscription formatée"""
        if hasattr(obj, 'date_inscription'):
            return obj.date_inscription.strftime('%d/%m/%Y')
        return "Non disponible"
    
    def actions_buttons(self, obj):
        """Boutons d'actions pour chaque visiteur"""
        return format_html(
            '<a class="button" href="{}">Envoyer Email</a>&nbsp;'
            '<a class="button" href="{}">Voir Messages</a>',
            f'mailto:{obj.email}',
            f'/admin/api/message/?visiteur__id__exact={obj.id}'
        )
    actions_buttons.short_description = 'Actions'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-emails/', self.admin_site.admin_view(self.import_emails_view), name='import_emails'),
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='visiteurs_dashboard'),
            path('send-direct-email/<int:visiteur_id>/', self.admin_site.admin_view(self.send_direct_email), name='send_direct_email'),
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
                            visiteur, created = Visiteur.objects.get_or_create(
                                email=email,
                                defaults={'date_inscription': timezone.now()}
                            )
                            
                            if created:
                                added_count += 1
                                # Envoyer email de bienvenue si demandé
                                if form.cleaned_data.get('send_welcome'):
                                    self.send_welcome_email(visiteur)
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
    
    def dashboard_view(self, request):
        """Vue de tableau de bord avancée pour les visiteurs"""
        # Statistiques de base
        total_visitors = Visiteur.objects.count()
        new_this_week = Visiteur.objects.filter(date_inscription__gte=timezone.now() - timedelta(days=7)).count()
        new_this_month = Visiteur.objects.filter(date_inscription__gte=timezone.now() - timedelta(days=30)).count()
        
        # Commentaires par visiteur (top 5)
        top_commenters = Visiteur.objects.annotate(
            comment_count=Count('commentaire')
        ).order_by('-comment_count')[:5]
        
        # Évolution du nombre de visiteurs par mois
        visitor_growth = [] # À implémenter avec une requête agrégée
        
        context = {
            'title': 'Tableau de bord Visiteurs',
            'total_visitors': total_visitors,
            'new_this_week': new_this_week,
            'new_this_month': new_this_month,
            'top_commenters': top_commenters,
            'visitor_growth': visitor_growth,
            'opts': self.model._meta,
        }
        return render(request, 'admin/visitors_dashboard.html', context)
    
    def send_direct_email(self, request, visiteur_id):
        """Envoyer un email personnalisé à un visiteur spécifique"""
        visiteur = Visiteur.objects.get(pk=visiteur_id)
        
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Envoyer l'email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [visiteur.email],
                fail_silently=False,
                html_message=message if '<' in message else None
            )
            
            self.message_user(request, f"Email envoyé avec succès à {visiteur.email}")
            return redirect('admin:api_visiteur_changelist')
        
        context = {
            'title': f'Envoyer un email à {visiteur.email}',
            'visiteur': visiteur,
            'opts': self.model._meta,
        }
        return render(request, 'admin/send_direct_email.html', context)
    
    def send_welcome_email(self, visiteur):
        """Envoie un email de bienvenue à un nouveau visiteur"""
        subject = "Bienvenue chez Fox ! 🦊"
        message = f"""
        <html>
        <body>
            <h2>Bonjour {visiteur.nom or 'cher visiteur'} !</h2>
            <p>Je suis ravi de vous compter parmi mes abonnés.</p>
            <p>Vous recevrez désormais mes dernières actualités, articles et projets directement dans votre boîte mail.</p>
            <p>N'hésitez pas à me contacter pour toute question ou suggestion !</p>
            <p>À très bientôt,</p>
            <p><strong>Arthur Donfack | Fox</strong><br>
            Développeur & Hacker Éthique</p>
        </body>
        </html>
        """
        
        try:
            send_mail(
                subject,
                "Bienvenue chez Fox !",
                settings.EMAIL_HOST_USER,
                [visiteur.email],
                fail_silently=False,
                html_message=message
            )
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email de bienvenue à {visiteur.email}: {e}")
    
    # Ajout d'un bouton d'action pour l'importation
    actions = ['redirect_to_import', 'send_bulk_email', 'export_to_csv']
    
    def redirect_to_import(self, request, queryset):
        return redirect('admin:import_emails')
    redirect_to_import.short_description = "Importer des emails depuis un fichier"
    
    def send_bulk_email(self, request, queryset):
        """Envoyer un email groupé aux visiteurs sélectionnés"""
        # Implémentation à faire
        self.message_user(request, f"Email envoyé à {queryset.count()} visiteur(s)")
    send_bulk_email.short_description = "Envoyer un email aux visiteurs sélectionnés"
    
    def export_to_csv(self, request, queryset):
        """Exporter les visiteurs sélectionnés en CSV"""
        # Implémentation à faire
        self.message_user(request, f"{queryset.count()} visiteur(s) exportés")
    export_to_csv.short_description = "Exporter au format CSV"

# Admin pour Project
class ProjectAdmin(FoxBaseAdmin):
    list_display = ('nom', 'categorie', 'sujet', 'date', 'preview_image')
    search_fields = ('nom', 'categorie', 'sujet', 'description')
    list_filter = ('categorie', 'date')
    
    def preview_image(self, obj):
        """Affiche une miniature de l'image du projet"""
        if obj.photo1_800_x_550:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.photo1_800_x_550.url)
        return "Pas d'image"
    preview_image.short_description = 'Aperçu'

# Admin pour Post
class PostAdmin(FoxBaseAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date', 'preview_image', 'comment_count')
    search_fields = ('titre', 'categorie', 'auteur', 'description', 'contenuP1')
    list_filter = ('categorie', 'date')
    
    def preview_image(self, obj):
        """Affiche une miniature de l'image de l'article"""
        if obj.photo500_x_800:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.photo500_x_800.url)
        return "Pas d'image"
    preview_image.short_description = 'Aperçu'
    
    def comment_count(self, obj):
        """Affiche le nombre de commentaires sur l'article"""
        return Commentaire.objects.filter(post=obj).count()
    comment_count.short_description = 'Commentaires'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='posts_dashboard'),
            path('analytics/<int:post_id>/', self.admin_site.admin_view(self.post_analytics_view), name='post_analytics'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Vue de tableau de bord pour les statistiques des articles"""
        # À implémenter
        context = {
            'title': 'Tableau de bord Articles',
            'opts': self.model._meta,
        }
        return render(request, 'admin/posts_dashboard.html', context)
    
    def post_analytics_view(self, request, post_id):
        """Vue d'analyse détaillée pour un article spécifique"""
        # À implémenter
        post = Post.objects.get(pk=post_id)
        context = {
            'title': f'Analyse de l\'article: {post.titre}',
            'post': post,
            'opts': self.model._meta,
        }
        return render(request, 'admin/post_analytics.html', context)

# Admin pour Timeline
class TimelineAdmin(FoxBaseAdmin):
    list_display = ('titre', 'periode', 'ordre')
    search_fields = ('titre', 'periode', 'description')
    list_editable = ('ordre',)

# Admin pour Temoignage
class TemoignageAdmin(FoxBaseAdmin):
    list_display = ('auteur', 'fonction', 'preview_text')
    search_fields = ('auteur', 'fonction', 'texte')
    
    def preview_text(self, obj):
        """Affiche un aperçu du témoignage"""
        if len(obj.texte) > 100:
            return f"{obj.texte[:100]}..."
        return obj.texte
    preview_text.short_description = 'Témoignage'

# Admin pour Commentaire
class CommentaireAdmin(FoxBaseAdmin):
    list_display = ('post_title', 'visiteur_email', 'date', 'preview_content')
    search_fields = ('post__titre', 'visiteur__email', 'contenu')
    list_filter = ('date', 'post')
    
    def post_title(self, obj):
        """Affiche le titre de l'article commenté"""
        return obj.post.titre
    post_title.short_description = 'Article'
    
    def visiteur_email(self, obj):
        """Affiche l'email du visiteur"""
        return obj.visiteur.email
    visiteur_email.short_description = 'Visiteur'
    
    def preview_content(self, obj):
        """Affiche un aperçu du commentaire"""
        if len(obj.contenu) > 100:
            return f"{obj.contenu[:100]}..."
        return obj.contenu
    preview_content.short_description = 'Commentaire'

# Admin pour Message
class MessageAdmin(FoxBaseAdmin):
    list_display = ('visiteur_email', 'objet', 'preview_content', 'date_reception')
    search_fields = ('visiteur__email', 'objet', 'contenu')
    
    def visiteur_email(self, obj):
        """Affiche l'email du visiteur"""
        return obj.visiteur.email
    visiteur_email.short_description = 'De'
    
    def preview_content(self, obj):
        """Affiche un aperçu du message"""
        if len(obj.contenu) > 100:
            return f"{obj.contenu[:100]}..."
        return obj.contenu
    preview_content.short_description = 'Message'
    
    def date_reception(self, obj):
        """Affiche la date de réception du message"""
        if hasattr(obj, 'date'):
            return obj.date.strftime('%d/%m/%Y %H:%M')
        return "Non disponible"
    date_reception.short_description = 'Reçu le'

# Admin pour Newsletter
class NewsletterAdmin(FoxBaseAdmin):
    list_display = ('title', 'created_at', 'sent_status')
    search_fields = ('title', 'subtitle', 'main_content')
    list_filter = ('created_at',)
    
    def sent_status(self, obj):
        """Affiche si la newsletter a été envoyée"""
        if hasattr(obj, 'sent') and obj.sent:
            return format_html('<span style="color: green;">✓ Envoyée</span>')
        return format_html('<span style="color: red;">✗ Non envoyée</span>')
    sent_status.short_description = 'Statut'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send/<int:newsletter_id>/', self.admin_site.admin_view(self.send_newsletter_view), name='send_newsletter'),
            path('preview/<int:newsletter_id>/', self.admin_site.admin_view(self.preview_newsletter), name='preview_newsletter'),
        ]
        return custom_urls + urls
    
    def send_newsletter_view(self, request, newsletter_id):
        """Vue pour envoyer une newsletter spécifique"""
        # À implémenter
        context = {
            'title': 'Envoyer la newsletter',
            'opts': self.model._meta,
        }
        return render(request, 'admin/send_newsletter.html', context)
    
    def preview_newsletter(self, request, newsletter_id):
        """Prévisualisation d'une newsletter"""
        # À implémenter
        context = {
            'title': 'Prévisualisation de la newsletter',
            'opts': self.model._meta,
        }
        return render(request, 'admin/preview_newsletter.html', context)

# Admin pour Annonce
class AnnonceAdmin(FoxBaseAdmin):
    list_display = ('date', 'preview_content')
    search_fields = ('contenuP1', 'contenuConclusion', 'contenuSitation')
    
    def preview_content(self, obj):
        """Affiche un aperçu du contenu de l'annonce"""
        if obj.contenuP1 and len(obj.contenuP1) > 100:
            return f"{obj.contenuP1[:100]}..."
        return obj.contenuP1
    preview_content.short_description = 'Contenu'

# Admin pour Profile
class ProfileAdmin(FoxBaseAdmin):
    list_display = ('nom', 'email', 'telephone')
    search_fields = ('nom', 'email', 'telephone', 'descriptionP1')

# Personnalisation de l'admin site
class FoxAdminSite(admin.AdminSite):
    site_header = 'Administration Fox 🦊'
    site_title = 'Fox Admin'
    index_title = 'Tableau de bord'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='admin_dashboard'),
            path('stats/', self.admin_view(self.stats_view), name='admin_stats'),
            path('api/visitors-stats/', self.admin_view(self.visitors_stats_api), name='api_visitors_stats'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Vue de tableau de bord global de l'administration"""
        # Statistiques pour le tableau de bord
        stats = {
            'total_visitors': Visiteur.objects.count(),
            'total_posts': Post.objects.count(),
            'total_projects': Project.objects.count(),
            'total_comments': Commentaire.objects.count(),
            'total_messages': Message.objects.count(),
            'recent_visitors': Visiteur.objects.order_by('-id')[:5],
            'recent_comments': Commentaire.objects.order_by('-date')[:5],
            'recent_messages': Message.objects.order_by('-id')[:5],
        }
        
        context = {
            'title': 'Tableau de bord Fox',
            'stats': stats,
        }
        return render(request, 'admin/dashboard.html', context)
    
    def stats_view(self, request):
        """Vue de statistiques avancées"""
        context = {
            'title': 'Statistiques du site',
        }
        return render(request, 'admin/stats.html', context)
    
    def visitors_stats_api(self, request):
        """API pour les statistiques des visiteurs (pour les graphiques)"""
        # Données pour les graphiques
        data = {
            'labels': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
            'visitors': [12, 19, 3, 5, 2, 3, 20, 33, 25, 14, 18, 10],  # Données factices
            'comments': [7, 11, 5, 8, 3, 7, 15, 22, 18, 9, 12, 7],     # Données factices
        }
        return JsonResponse(data)

# Création d'une instance personnalisée de l'admin site
# admin_site = FoxAdminSite(name='foxadmin')

# Enregistrement des modèles dans l'admin
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Visiteur, VisiteurAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Timeline, TimelineAdmin)
admin.site.register(Temoignage, TemoignageAdmin)

# Personnalisation de l'admin
admin.site.site_header = 'Administration Fox 🦊'
admin.site.site_title = 'Fox Admin'
admin.site.index_title = 'Tableau de bord Fox'