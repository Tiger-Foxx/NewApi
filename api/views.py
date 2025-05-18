from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime

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