from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .authentication import ExpiringTokenAuthentication
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import (
    Profile, Project, Post, Visiteur, Commentaire, 
    Message, Annonce, Newsletter, Timeline, Temoignage
)
from .serializers import (
    ProfileSerializer, ProjectSerializer, PostSerializer, 
    VisiteurSerializer, CommentaireSerializer, MessageSerializer,
    AnnonceSerializer, NewsletterSerializer, TimelineSerializer,
    TemoignageSerializer, SubscribeSerializer
)

# ViewSets pour les ressources principales
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('-date')
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        queryset = Project.objects.all().order_by('-date')
        categorie = self.request.query_params.get('categorie', None)
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        return queryset

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all().order_by('-date')
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date')
        categorie = self.request.query_params.get('categorie', None)
        if categorie:
            queryset = queryset.filter(categorie=categorie)
        return queryset

class TimelineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Timeline.objects.all().order_by('ordre')
    serializer_class = TimelineSerializer

class TemoignageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer

# Fonctions pour les opérations spécifiques
@api_view(['POST'])
def subscribe(request):
    serializer = SubscribeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        nom = serializer.validated_data.get('nom', '')
        
        # Vérification de l'existence du visiteur
        if Visiteur.objects.filter(email=email).exists():
            message = f"Merci ! {email} Vous recevez déjà nos nouvelles par e-mail !"
        else:
            # Création et enregistrement du visiteur
            visiteur = Visiteur.objects.create(email=email, nom=nom)
            message = f"Merci ! {email} Vous recevrez nos nouvelles par e-mail !"

            # Envoi des e-mails
            envoyer_email(
                message='Merci de votre visite ! Vous recevrez toutes les dernières NEWS Tech de FOX, BISOU',
                email=email, 
                sujet='BIENVENUE CHEZ FOX !!!'
            )
            envoyer_email(
                message=f"Un nouveau souscrivant à votre Newsletter, il s'agit de : {email}",
                email="donfackarthur750@gmail.com", 
                sujet=f'NOUVEAU SOUSCRIVANT NEWSLETTER : {email}'
            )

        return Response({'message': message}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    email = request.data.get('email')
    nom = request.data.get('nom', '')
    contenu = request.data.get('contenu')
    
    if not email or not contenu:
        return Response(
            {'error': 'Email et contenu sont requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Création ou récupération du visiteur
    visiteur, created = Visiteur.objects.get_or_create(
        email=email,
        defaults={'nom': nom}
    )
    
    # Mise à jour du nom si le visiteur existe déjà
    if not created and nom:
        visiteur.nom = nom
        visiteur.save()
    
    # Création du commentaire
    commentaire = Commentaire.objects.create(
        visiteur=visiteur,
        post=post,
        contenu=contenu
    )
    
    serializer = CommentaireSerializer(commentaire)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def send_message(request):
    email = request.data.get('email')
    nom = request.data.get('nom', '')
    objet = request.data.get('objet', '')
    contenu = request.data.get('contenu')
    
    if not email or not contenu:
        return Response(
            {'error': 'Email et contenu sont requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Création ou récupération du visiteur
    visiteur, created = Visiteur.objects.get_or_create(
        email=email,
        defaults={'nom': nom}
    )
    
    # Mise à jour du nom si le visiteur existe déjà
    if not created and nom:
        visiteur.nom = nom
        visiteur.save()
    
    # Création du message
    message = Message.objects.create(
        visiteur=visiteur,
        objet=objet,
        contenu=contenu
    )
    
    # Envoi email de notification
    envoyer_email(
        message=contenu,
        sujet=f'NOUVEAU MESSAGE SUR LE SITE FOX: {objet}',
        email='donfackarthur750@gmail.com'
    )
    
    return Response(
        {'message': f'Merci {nom} pour votre message !'},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_newsletter(request):
    title = request.data.get('title')
    subtitle = request.data.get('subtitle', '')
    main_content = request.data.get('main_content')
    quote = request.data.get('quote', '')
    conclusion = request.data.get('conclusion')
    image_url = request.data.get('image_url', '')
    article_url = request.data.get('article_url', '')
    
    if not title or not main_content or not conclusion:
        return Response(
            {'error': 'Titre, contenu principal et conclusion sont requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Création de la newsletter
    newsletter = Newsletter.objects.create(
        title=title,
        subtitle=subtitle,
        main_content=main_content,
        quote=quote,
        conclusion=conclusion,
        image_url=image_url,
        article_url=article_url
    )
    
    profile = Profile.objects.first()
    
    # Contexte pour le template
    context = {
        'newsletter': newsletter,
        'year': datetime.now().year,
        'profile': profile,
    }
    
    # Génération du contenu HTML
    html_content = render_to_string('email/newsletter_template.html', context)
    text_content = strip_tags(html_content)  # Version texte pour fallback
    
    # Préparation et envoi de l'email
    subject = f"Fox : {newsletter.title}"
    
    for subscriber in Visiteur.objects.all():
        try:
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(f"Erreur d'envoi à {subscriber.email}: {e}")
    
    return Response(
        {'message': 'Newsletter envoyée avec succès! 🎉'},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_announcement(request):
    contenuP1 = request.data.get('contenuP1')
    contenuConclusion = request.data.get('contenuConclusion', '')
    contenuSitation = request.data.get('contenuSitation', '')
    image_url = request.data.get('image_url', '')
    
    if not contenuP1:
        return Response(
            {'error': 'Le contenu principal est requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Création de l'annonce
    annonce = Annonce.objects.create(
        contenuP1=contenuP1,
        contenuConclusion=contenuConclusion,
        contenuSitation=contenuSitation
    )
    
    sujet = "NOUVELLE ANNONCE DE FOX, TON RENARD PREF HAHA !"
    
    # Construire le contenu HTML de l'email
    message_html = f"""
    <html>
        <body>
            <h2>Hey ! Nouvelle Annonce de FOX</h2>
            <p><strong>{annonce.contenuP1}</strong></p>
            <blockquote>{annonce.contenuSitation}</blockquote>
            <p><b>{annonce.contenuConclusion}</b></p>
            {'<img src="'+image_url+'">' if image_url else ''}
        </body>
    </html>
    """
    
    # Envoi de l'email HTML à tous les visiteurs
    visiteurs = Visiteur.objects.all()
    for visiteur in visiteurs:
        envoyer_email_html(visiteur.email, sujet, message_html)
    
    return Response(
        {'message': 'Annonce publiée et envoyée avec succès!'},
        status=status.HTTP_201_CREATED
    )

# Fonctions utilitaires pour l'envoi d'emails
def envoyer_email(email, sujet, message):
    try:
        send_mail(
            sujet,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        print(f"Email envoyé avec succès à {email}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email à {email}: {e}")
        return False

def envoyer_email_html(email, sujet, message_html):
    try:
        text_content = strip_tags(message_html)
        msg = EmailMultiAlternatives(
            sujet,
            text_content,
            settings.EMAIL_HOST_USER,
            [email]
        )
        msg.attach_alternative(message_html, "text/html")
        msg.send()
        print(f"Email HTML envoyé avec succès à {email}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email HTML à {email}: {e}")
        return False
    


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Si le token existe déjà, on le renouvelle
        if not created:
            token.created = timezone.now()
            token.save()
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([ExpiringTokenAuthentication])
def change_password(request):
    """Permet à un utilisateur authentifié de changer son mot de passe"""
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(current_password):
        return Response({'error': 'Mot de passe actuel incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Mot de passe changé avec succès'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([ExpiringTokenAuthentication])
def get_user_info(request):
    """Récupère les informations de l'utilisateur connecté"""
    user = request.user
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined,
    })

@api_view(['POST'])
@csrf_exempt
def track_visitor(request):
    """
    Enregistre une visite sur le site et notifie par email
    Cette route est publique et peut être appelée par le frontend
    """
    # Récupération des données du visiteur
    ip_address = request.META.get('REMOTE_ADDR', 'Inconnue')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Inconnu')
    page_visited = request.data.get('page', '/')
    referrer = request.data.get('referrer', 'Direct')
    
    # Formatage du message
    message = f"""
    Nouvelle visite sur votre site Fox !
    
    Date et heure : {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}
    Page visitée : {page_visited}
    Adresse IP : {ip_address}
    Navigateur : {user_agent}
    Référent : {referrer}
    """
    
    # Envoi de l'email de notification
    send_mail(
        'Nouvelle visite sur votre site Fox 🦊',
        message,
        settings.EMAIL_HOST_USER,
        ['donfackarthur750@gmail.com'],
        fail_silently=True
    )
    
    return Response({'status': 'success'}, status=status.HTTP_200_OK)

# Ajouter cette vue aux vues existantes
@api_view(['GET'])
def dashboard_stats(request):
    """
    Fournit des statistiques pour le tableau de bord du frontend
    """
    # Comptages généraux
    total_projects = Project.objects.count()
    total_posts = Post.objects.count()
    total_testimonials = Temoignage.objects.count()
    
    # Articles récents
    recent_posts = Post.objects.order_by('-date')[:3]
    recent_posts_data = PostSerializer(recent_posts, many=True).data
    
    # Projets récents
    recent_projects = Project.objects.order_by('-date')[:3]
    recent_projects_data = ProjectSerializer(recent_projects, many=True).data
    
    # Témoignages aléatoires
    testimonials = Temoignage.objects.order_by('?')[:3]
    testimonials_data = TemoignageSerializer(testimonials, many=True).data
    
    # Statistiques globales
    stats = {
        'totalProjects': total_projects,
        'totalPosts': total_posts,
        'totalTestimonials': total_testimonials,
        'recentPosts': recent_posts_data,
        'recentProjects': recent_projects_data,
        'testimonials': testimonials_data,
    }
    
    return Response(stats)
