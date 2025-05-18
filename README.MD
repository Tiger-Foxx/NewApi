# 🦊 FOX API - Backend Premium pour Portfolio de Développeur & Hacker Éthique

<div align="center">
  <img src="https://github.com/Tiger-Foxx/BlueLightFox/raw/main/FoxyBlueLight/Resources/logo.png" alt="Fox API Logo" width="200"/>
  <h3>Arthur Donfack | Développeur & Hacker Éthique</h3>
  <p><em>"Fox, life is easier: The genius at the disposal of all your dreams."</em></p>
</div>

**Date de dernière mise à jour:** 2025-05-18

## 📋 Table des matières

- [Introduction](#-introduction)
- [Contexte et vision](#-contexte-et-vision)
- [Architecture technique](#-architecture-technique)
- [Configuration du projet](#-configuration-du-projet)
- [Modèles de données](#-modèles-de-données)
- [API Endpoints](#-api-endpoints)
- [Authentification](#-authentification)
- [Administration](#-administration)
- [Emails et Notifications](#-emails-et-notifications)
- [Déploiement](#-déploiement)
- [Attentes frontend](#-attentes-frontend)
- [Structure des articles](#-structure-des-articles)
- [Timeline interactive](#-timeline-interactive)
- [À propos de l'auteur](#-à-propos-de-lauteur)
- [Ressources et liens](#-ressources-et-liens)
- [Licence](#-licence)

## 🚀 Introduction

Fox API est le backend premium développé pour la plateforme professionnelle d'Arthur Donfack, alias "Fox" ou "The Tiger Fox". Cette API RESTful constitue l'épine dorsale d'un écosystème digital comprenant un portfolio de développeur, un blog technique, et une vitrine de services en ingénierie informatique (développement, cybersécurité, formation).

Ce repository contient une API Django REST Framework complète, née d'une refactorisation majeure transformant une application Django monolithique en architecture moderne API-first. Cette approche permet au frontend de se concentrer exclusivement sur l'expérience utilisateur sans compromis sur la performance ou les fonctionnalités.

### Technologies principales

- **Django 4.2.11** - Framework backend robuste
- **Django REST Framework 3.14.0** - Extension API RESTful
- **SQLite/PostgreSQL** - Persistence des données
- **JWT Authentication** - Sécurisation des endpoints
- **CORS Headers** - Communication cross-origin sécurisée
- **Whitenoise** - Servir les fichiers statiques efficacement
- **Pillow** - Manipulation d'images
- **EmailMultiAlternatives** - Emails HTML responsifs

## 🧠 Contexte et vision

### Genèse du projet

Ce projet est issu d'une refonte architecturale complète du site personnel et professionnel de Fox. L'implémentation précédente utilisait Django comme framework monolithique (backend + frontend), où les vues rendaient directement des templates HTML. Cette approche présentait plusieurs limitations majeures :

1. **Expérience utilisateur limitée** - Navigation avec rechargements complets de page
2. **Difficulté d'évolution** - Couplage fort entre logique métier et présentation
3. **Performance sous-optimale** - Génération côté serveur de pages complètes
4. **Flexibilité restreinte** - Limitations pour les interactions riches côté client
5. **Maintenabilité complexe** - Modifications frontend nécessitant des changements backend

Après analyse, la décision a été prise de transformer l'application en architecture moderne découplée :

- **Backend** : API RESTful pure (Django REST Framework)
- **Frontend** : Single Page Application (SPA) React indépendante

Cette architecture offre une expérience utilisateur fluide, des développements parallélisables et une maintenabilité grandement améliorée.

### Migration des données existantes

Un défi majeur consistait à préserver l'intégrité des données existantes tout en restructurant l'architecture. Une stratégie soigneusement élaborée a permis de maintenir les structures de tables d'origine :

```python
# Extrait de configuration pour maintenir la compatibilité avec les tables existantes
class Post(models.Model):
    # Champs du modèle avec structure d'origine
    titre = models.CharField(max_length=328)
    description = models.TextField()
    # ...
    
    class Meta:
        # Pointe explicitement vers la table existante
        db_table = 'FoxApp_post'
```

Cette approche assure la continuité du service et préserve l'historique tout en offrant les avantages d'une architecture moderne.

## 🏗 Architecture technique

### Structure du projet

```
FoxAPI/
├── FoxAPI/                 # Configuration du projet Django
│   ├── settings.py         # Paramètres globaux et env variables
│   ├── urls.py             # Routage principal
│   └── wsgi.py             # Configuration de déploiement
├── api/                    # Application API principale
│   ├── models/             # Modèles de données
│   │   ├── __init__.py     # Import des modèles
│   │   ├── profile.py      # Modèle de profil personnel
│   │   ├── project.py      # Modèle de projets/portfolio
│   │   ├── post.py         # Modèle d'articles/blog
│   │   ├── visitor.py      # Modèle de visiteurs/abonnés
│   │   └── ...             # Autres modèles
│   ├── serializers.py      # Convertisseurs Python ↔ JSON
│   ├── views.py            # Logique des endpoints API
│   ├── urls.py             # Définition des routes API
│   ├── admin.py            # Administration personnalisée
│   ├── authentication.py   # Système d'authentification custom
│   └── permissions.py      # Gestion des permissions
├── templates/              # Templates pour emails et admin
│   ├── admin/              # Templates d'administration améliorés
│   │   ├── dashboard.html  # Tableau de bord personnalisé
│   │   └── ...             # Autres templates admin
│   └── email/              # Templates d'emails HTML
│       ├── newsletter.html # Template de newsletter
│       └── ...             # Autres templates email
├── media/                  # Fichiers uploadés (images, etc.)
│   ├── PhotoFox/           # Images des posts, projets, profil
│   └── FilesFox/           # PDF, fichiers téléchargeables
├── static/                 # Fichiers statiques (CSS, JS)
│   ├── css/                # Styles pour l'admin
│   └── js/                 # Scripts pour l'admin
└── manage.py               # Utilitaire de gestion Django
```

### Composants architecturaux clés

#### 1. API RESTful

L'API suit les principes REST avec:
- **Points d'entrée standardisés** pour chaque ressource
- **CRUD complet** (Create, Read, Update, Delete)
- **Pagination** pour les listes longues
- **Filtrage et recherche** sur les champs pertinents
- **Sérialisation/Désérialisation** JSON cohérente
- **Gestion d'erreurs** standardisée

#### 2. Authentification & Sécurité

Système d'authentification robuste incluant:
- **Tokens avec expiration** pour sécuriser l'accès
- **Protection CSRF** pour les requêtes sensibles
- **Permissions granulaires** basées sur les rôles
- **Rate limiting** pour prévenir les abus
- **Headers sécurisés** contre les attaques XSS/CSRF

#### 3. Media Management

Gestion avancée des médias:
- **Upload d'images optimisé** avec validation
- **Redimensionnement automatique** des images
- **Stockage efficace** avec nommage structuré
- **Sécurisation des accès** aux fichiers sensibles

#### 4. Email Engine

Système d'emails sophistiqué:
- **Templates HTML responsifs** avec marque Fox
- **Versions texte fallback** automatiques
- **File d'attente asynchrone** pour envois massifs
- **Personnalisation dynamique** par destinataire

#### 5. Administration améliorée

Interface administrateur sur mesure:
- **Tableaux de bord** avec KPI et visualisations
- **Actions en masse** pour la gestion de contenu
- **Import/Export** de données en divers formats
- **Interface utilisateur améliorée** pour la productivité

## ⚙️ Configuration du projet

### Prérequis

- Python 3.10+
- pip (dernière version)
- Virtualenv ou équivalent
- Git

### Installation

```bash
# Cloner le repository
git clone https://github.com/theTigerFox/fox-api.git
cd fox-api

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

### Configuration des variables d'environnement

Pour le développement, créez un fichier `.env` à la racine du projet:

```env
# Environnement (development, staging, production)
ENV=development

# Clé secrète Django (à changer en production)
SECRET_KEY=votre-cle-secrete-ici

# Configuration des emails
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tigerfox750@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
EMAIL_USE_TLS=True

# URLs autorisées
ALLOWED_HOSTS=localhost,127.0.0.1,theoldfox.pythonanywhere.com

# Configuration CORS pour le frontend
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://foxdev.netlify.app

# Expiration token (en secondes) - 7 jours
TOKEN_EXPIRED_AFTER_SECONDS=604800
```

## 📊 Modèles de données

L'API est construite autour des modèles principaux suivants:

### Profile

Représente les informations personnelles et professionnelles de Fox.

```python
class Profile(models.Model):
    nom = models.CharField(max_length=328)
    sousTitre = models.TextField()
    photo = models.ImageField(upload_to='PhotoFox')
    descriptionP1 = models.TextField()
    descriptionP2 = models.TextField()
    signature = models.ImageField(upload_to='PhotoFox')
    email = models.EmailField()
    telephone = models.CharField(max_length=328)
    cv = models.FileField(upload_to='FilesFox', blank=True, null=True)
    facebook = models.URLField(blank=True)
    github = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    gmail = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    
    class Meta:
        db_table = 'FoxApp_profile'
```

### Project

Portfolio de projets réalisés, catégorisés par type et avec médias.

```python
class Project(models.Model):
    nom = models.CharField(max_length=328)
    description = models.TextField()
    photo1_800_x_550 = models.ImageField(upload_to='PhotoFox', blank=True)
    photo2_800_x_550 = models.ImageField(upload_to='PhotoFox', blank=True)
    photo3_800_x_550 = models.ImageField(upload_to='PhotoFox', blank=True)
    categorie = models.CharField(max_length=328)
    sujet = models.CharField(max_length=328, blank=True)
    date = models.DateField(blank=True)
    demo = models.URLField(blank=True)
    
    class Meta:
        db_table = 'FoxApp_project'
```

### Post

Articles de blog avec contenu HTML enrichi. **Le champ contenuP1 est le plus important** car il contient le code HTML complet de l'article dans une div, formant l'intégralité du contenu formaté.

```python
class Post(models.Model):
    titre = models.CharField(max_length=328)
    description = models.TextField()
    photo500_x_800 = models.ImageField(upload_to='PhotoFox')
    photo800_x_533 = models.ImageField(upload_to='PhotoFox', blank=True)
    categorie = models.CharField(max_length=328)
    auteur = models.CharField(max_length=328, blank=True)
    date = models.DateField(auto_now_add=True)
    # ↓↓↓ CHAMP PRINCIPAL - CONTIENT LE HTML COMPLET DE L'ARTICLE ↓↓↓
    contenuP1 = models.TextField(blank=True, null=True)  # Contient tout le HTML de l'article
    # Les champs ci-dessous seront supprimés dans une future version
    contenuP2 = models.TextField(blank=True, null=True)  # Déprécié
    contenuP3 = models.TextField(blank=True, null=True)  # Déprécié
    contenuP4 = models.TextField(blank=True, null=True)  # Déprécié
    contenuConclusion = models.TextField(blank=True, null=True)  # Déprécié
    contenuSitation = models.TextField(blank=True, null=True)  # Déprécié
    
    class Meta:
        db_table = 'FoxApp_post'
```

### Visiteur

Utilisateurs inscrits à la newsletter ou ayant interagi avec le site.

```python
class Visiteur(models.Model):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        db_table = 'FoxApp_visiteur'
```

### Commentaire

Commentaires sur les articles du blog.

```python
class Commentaire(models.Model):
    contenu = models.TextField()
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'FoxApp_commentaire'
```

### Message

Messages de contact envoyés via le formulaire du site.

```python
class Message(models.Model):
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    contenu = models.TextField()
    objet = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        db_table = 'FoxApp_message'
```

### Timeline

Parcours professionnel et académique affiché chronologiquement.

```python
class Timeline(models.Model):
    titre = models.CharField(max_length=200)
    periode = models.CharField(max_length=100)
    description = models.TextField()
    ordre = models.IntegerField(default=0)
```

### Temoignage

Retours clients et recommandations professionnelles.

```python
class Temoignage(models.Model):
    texte = models.TextField()
    auteur = models.CharField(max_length=100)
    fonction = models.CharField(max_length=150)
```

### Newsletter et Annonce

Gestion des campagnes email et communications.

```python
class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    main_content = models.TextField()
    quote = models.TextField(blank=True)
    conclusion = models.TextField()
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    article_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'FoxApp_newsletter'

class Annonce(models.Model):
    date = models.DateField(auto_now_add=True)
    contenuP1 = models.TextField(blank=True, null=True)
    contenuConclusion = models.TextField(blank=True, null=True)
    contenuSitation = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'FoxApp_annonce'
```

## 🔌 API Endpoints

L'API expose plusieurs endpoints pour accéder aux données et exécuter des actions. Voici une description détaillée de chaque endpoint avec des exemples de requêtes et réponses.

### Endpoints publics

Ces endpoints sont accessibles sans authentification.

#### Profile

```
GET /api/profile/
```

Retourne les informations du profil Fox.

**Exemple de réponse:**
```json
{
  "id": 1,
  "nom": "Arthur Donfack",
  "sousTitre": "Développeur & Hacker Éthique",
  "photo": "/media/PhotoFox/profile_pic.jpg",
  "descriptionP1": "Étudiant en génie informatique...",
  "descriptionP2": "Passionné par le développement web...",
  "signature": "/media/PhotoFox/signature.png",
  "email": "donfackarthur750@gmail.com",
  "telephone": "+237 658 866 639",
  "cv": "/media/FilesFox/Arthur_Donfack_CV.pdf",
  "facebook": "https://facebook.com/thetigerfox",
  "github": "https://github.com/theTigerFox",
  "instagram": "https://instagram.com/thetigerfox",
  "linkedIn": "https://linkedin.com/in/arthur-donfack",
  "gmail": "",
  "youtube": "https://youtube.com/c/FoxTechChannel"
}
```

#### Projets

```
GET /api/projects/
GET /api/projects/?categorie=security
GET /api/projects/{id}/
```

Liste et détail des projets réalisés, avec possibilité de filtrer par catégorie.

**Exemple de réponse:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nom": "FoxyBlueLight",
      "description": "Application de protection contre la lumière bleue...",
      "photo1_800_x_550": "/media/PhotoFox/foxybluelight_1.jpg",
      "photo2_800_x_550": "/media/PhotoFox/foxybluelight_2.jpg",
      "photo3_800_x_550": "/media/PhotoFox/foxybluelight_3.jpg",
      "categorie": "dev",
      "sujet": "Protection des yeux",
      "date": "2023-11-15",
      "demo": "https://github.com/theTigerFox/FoxyBlueLight"
    }
  ]
}
```

#### Articles (Posts)

```
GET /api/posts/
GET /api/posts/?categorie=cybersecurity
GET /api/posts/{id}/
```

Liste et détail des articles du blog, avec filtrage par catégorie. **Le champ contenuP1 contient le HTML complet de l'article** et doit être injecté directement dans le DOM (en utilisant dangerouslySetInnerHTML en React ou v-html en Vue.js).

**Exemple de réponse:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "titre": "Windows a un Filtre Lumière Bleue... Et J'ai Décidé de Lui Donner des Stéroïdes !",
      "description": "Comment j'ai développé FoxyBlueLight pour améliorer le filtre lumière bleue de Windows",
      "photo500_x_800": "/media/PhotoFox/foxybluelight_vertical.jpg",
      "photo800_x_533": "/media/PhotoFox/foxybluelight_banner.jpg",
      "categorie": "dev",
      "auteur": "Arthur Donfack",
      "date": "2023-12-10",
      "contenuP1": "<div class=\"container my-4\" style=\"max-width: 950px;\">...[HTML COMPLET DE L'ARTICLE]...</div>",
      "contenuP2": null,
      "contenuP3": null,
      "contenuP4": null,
      "contenuConclusion": null,
      "contenuSitation": null
    }
  ]
}
```

#### Timeline

```
GET /api/timeline/
```

Chronologie du parcours professionnel et académique, triée par ordre.

**Exemple de réponse:**
```json
[
  {
    "id": 1,
    "titre": "ML & IA pour sécurité réseau",
    "periode": "2024-Présent",
    "description": "Application du Machine Learning et de l'Intelligence Artificielle à la détection d'intrusions et à l'analyse comportementale des réseaux.",
    "ordre": 1
  },
  {
    "id": 2,
    "titre": "Spécialisation en sécurité informatique",
    "periode": "2023-2024",
    "description": "Certification en cybersécurité et hacking éthique. Analyse de vulnérabilités et tests d'intrusion.",
    "ordre": 2
  }
]
```

#### Témoignages

```
GET /api/temoignages/
```

Témoignages clients et recommandations professionnelles.

**Exemple de réponse:**
```json
[
  {
    "id": 1,
    "texte": "Arthur a développé une application sur mesure qui a transformé notre processus de gestion. Son professionnalisme et sa réactivité sont remarquables.",
    "auteur": "Jean Dupont",
    "fonction": "CEO, TechInnovate"
  },
  {
    "id": 2,
    "texte": "Fox possède une expertise rare en sécurité informatique. Il a identifié et corrigé des vulnérabilités critiques dans notre infrastructure que personne n'avait détectées.",
    "auteur": "Marie Laurent",
    "fonction": "CISO, SecureData"
  }
]
```

#### Statistiques du dashboard

```
GET /api/dashboard-stats/
```

Fournit des statistiques globales pour le dashboard du frontend.

**Exemple de réponse:**
```json
{
  "totalProjects": 8,
  "totalPosts": 12,
  "totalTestimonials": 5,
  "recentPosts": [...],
  "recentProjects": [...],
  "testimonials": [...]
}
```

### Endpoints interactifs

Ces endpoints permettent aux utilisateurs d'interagir avec le site.

#### Inscription à la newsletter

```
POST /api/subscribe/
```

**Corps de la requête:**
```json
{
  "email": "utilisateur@example.com",
  "nom": "John Doe"
}
```

**Réponse (201 Created):**
```json
{
  "message": "Merci ! utilisateur@example.com Vous recevrez nos nouvelles par e-mail !"
}
```

#### Ajouter un commentaire

```
POST /api/posts/{post_id}/comments/
```

**Corps de la requête:**
```json
{
  "email": "utilisateur@example.com",
  "nom": "John Doe",
  "contenu": "Article très intéressant ! J'aimerais en savoir plus sur les outils utilisés."
}
```

**Réponse (201 Created):**
```json
{
  "id": 1,
  "visiteur": 3,
  "post": 2,
  "contenu": "Article très intéressant ! J'aimerais en savoir plus sur les outils utilisés.",
  "date": "2025-05-18T09:30:45Z",
  "visiteur_email": "utilisateur@example.com",
  "visiteur_nom": "John Doe"
}
```

#### Envoyer un message

```
POST /api/send-message/
```

**Corps de la requête:**
```json
{
  "email": "client@example.com",
  "nom": "Alice Smith",
  "objet": "Demande de devis pour site e-commerce",
  "contenu": "Bonjour, je suis intéressé par vos services pour développer un site e-commerce. Pouvons-nous discuter des détails et du budget ?"
}
```

**Réponse (201 Created):**
```json
{
  "message": "Merci Alice Smith pour votre message !"
}
```

#### Tracking visiteur

```
POST /api/track-visitor/
```

**Corps de la requête:**
```json
{
  "page": "/projects",
  "referrer": "https://google.com"
}
```

**Réponse (200 OK):**
```json
{
  "status": "success"
}
```

### Endpoints administratifs

Ces endpoints nécessitent une authentification avec des privilèges d'administration.

#### Authentification

```
POST /api/auth/token/
```

**Corps de la requête:**
```json
{
  "username": "admin",
  "password": "mot_de_passe_sécurisé"
}
```

**Réponse (200 OK):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "email": "admin@example.com",
  "is_staff": true,
  "is_superuser": true
}
```

#### Informations utilisateur

```
GET /api/auth/user-info/
```

*Header:* `Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

**Réponse (200 OK):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "is_staff": true,
  "is_superuser": true,
  "date_joined": "2023-01-01T00:00:00Z"
}
```

#### Envoi de newsletter

```
POST /api/send-newsletter/
```

*Header:* `Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

**Corps de la requête:**
```json
{
  "title": "Nouvelles technologies de sécurité réseau",
  "subtitle": "Tendances et innovations 2025",
  "main_content": "<p>Dans cette newsletter, nous explorerons les dernières technologies...</p>",
  "quote": "La défense doit être parfaite, l'attaque doit trouver une seule faille.",
  "conclusion": "<p>Restez vigilants et à jour avec vos pratiques de sécurité...</p>",
  "image_url": "https://example.com/images/security-trends.jpg",
  "article_url": "https://fox-dev.com/blog/security-trends-2025"
}
```

**Réponse (200 OK):**
```json
{
  "message": "Newsletter envoyée avec succès! 🎉"
}
```

#### Envoi d'annonce

```
POST /api/send-announcement/
```

*Header:* `Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

**Corps de la requête:**
```json
{
  "contenuP1": "Nous sommes ravis d'annoncer le lancement de notre nouveau service de sécurité réseau basé sur l'IA !",
  "contenuConclusion": "Contactez-nous dès aujourd'hui pour une démonstration gratuite.",
  "contenuSitation": "Protégez votre infrastructure avec l'intelligence de demain.",
  "image_url": "https://example.com/images/ai-security.jpg"
}
```

**Réponse (201 Created):**
```json
{
  "message": "Annonce publiée et envoyée avec succès!"
}
```

## 🔐 Authentification

Le système d'authentification utilise un mécanisme de token avec expiration pour une sécurité renforcée.

### Mécanisme de token

```python
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Authentification par token avec expiration
    """
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token invalide')

        # Vérification de l'expiration du token
        token_lifetime = getattr(settings, 'TOKEN_EXPIRED_AFTER_SECONDS', None)
        
        if token_lifetime is not None:
            expiration_date = token.created + timedelta(seconds=token_lifetime)
            
            if expiration_date < timezone.now():
                token.delete()
                raise AuthenticationFailed('Token expiré')

        if not token.user.is_active:
            raise AuthenticationFailed('Utilisateur désactivé')

        return (token.user, token)
```

### Utilisation côté client

Pour utiliser l'API avec authentification depuis le frontend, il faut:

1. **Obtenir un token**:

```javascript
const login = async (username, password) => {
  try {
    const response = await fetch('https://api.fox-dev.com/api/auth/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    if (!response.ok) {
      throw new Error('Erreur d\'authentification');
    }
    
    const data = await response.json();
    localStorage.setItem('foxAuthToken', data.token);
    return data;
  } catch (error) {
    console.error('Erreur de connexion:', error);
    throw error;
  }
};
```

2. **Utiliser le token pour les requêtes authentifiées**:

```javascript
const getAdminData = async () => {
  const token = localStorage.getItem('foxAuthToken');
  
  if (!token) {
    throw new Error('Non authentifié');
  }
  
  try {
    const response = await fetch('https://api.fox-dev.com/api/auth/user-info/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    
    if (response.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('foxAuthToken');
      throw new Error('Session expirée');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erreur:', error);
    throw error;
  }
};
```

## 📊 Administration

L'interface d'administration a été entièrement personnalisée pour offrir une expérience améliorée avec des tableaux de bord, des actions en masse et des visualisations.

### Tableaux de bord avancés

Le backend inclut des tableaux de bord riches pour la supervision:

- Statistiques de visites et d'interactions
- Graphiques d'évolution
- Liste des dernières activités
- Actions rapides

### Gestion des visiteurs

L'admin permet une gestion avancée des abonnés:

- Import/export d'emails en masse
- Segmentation et filtrage
- Envoi d'emails ciblés
- Analyses comportementales

### Gestion de contenu

Les fonctionnalités d'administration du contenu comprennent:

- Éditeur enrichi avec prévisualisation
- Planification de publications
- Gestion des médias avec prévisualisation
- Commentaires et modération

### Structure personnalisée

```python
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
```

## 📧 Emails et Notifications

Le système dispose d'un moteur d'emailing avancé pour les newsletters, confirmations et notifications.

### Templates HTML responsifs

Les emails utilisent des templates HTML modernes compatibles avec tous les clients mail:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ newsletter.title }}</title>
    <style>
        /* Styles responsifs pour emails */
        body {
            margin: 0;
            padding: 0;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #0F172A;
            color: #E2E8F0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #1E293B;
            border-radius: 16px;
            overflow: hidden;
        }
        .header {
            padding: 36px 0 25px;
            text-align: center;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        }
        .logo {
            color: #FDE047;
            font-size: 28px;
            font-weight: bold;
            margin: 0;
        }
        .tagline {
            color: #E2E8F0;
            margin: 5px 0 0;
            font-size: 14px;
        }
        /* Plus de styles... */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="logo">FOX</h1>
            <p class="tagline">SERVICE D'INGÉNIERIE INFORMATIQUE</p>
        </div>
        
        <div class="content">
            <h2 class="title">{{ newsletter.title }}</h2>
            {% if newsletter.subtitle %}
            <p class="subtitle">{{ newsletter.subtitle }}</p>
            {% endif %}
            
            {% if newsletter.image_url %}
            <img src="{{ newsletter.image_url }}" alt="Illustration" class="main-image">
            {% endif %}
            
            <div class="main-text">
                {{ newsletter.main_content|safe }}
            </div>
            
            {% if newsletter.quote %}
            <blockquote class="quote">
                {{ newsletter.quote }}
            </blockquote>
            {% endif %}
            
            <div class="conclusion">
                {{ newsletter.conclusion|safe }}
            </div>
            
            {% if newsletter.article_url %}
            <a href="{{ newsletter.article_url }}" class="button">Lire l'article complet</a>
            {% endif %}
        </div>
        
        <div class="footer">
            <p class="signature">Arthur Donfack | Fox</p>
            <p class="role">Développeur & Hacker Éthique</p>
            <p class="copyright">© {{ year }} Fox. Tous droits réservés.</p>
            <p class="contact">
                <a href="mailto:{{ profile.email }}">{{ profile.email }}</a> | 
                <a href="tel:{{ profile.telephone }}">{{ profile.telephone }}</a>
            </p>
        </div>
    </div>
</body>
</html>
```

### Processus d'envoi

Le système utilise un mécanisme robuste pour l'envoi d'emails:

```python
def send_newsletter(request):
    """Envoie la newsletter à tous les abonnés"""
    title = request.data.get('title')
    # ... autres champs
    
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
```

### Notifications système

Le backend inclut des notifications pour les événements importants:

- Nouvelle visite sur le site
- Nouvel abonné à la newsletter
- Nouveau message de contact
- Nouveau commentaire sur un article

## 🚀 Déploiement

La configuration de déploiement est optimisée pour PythonAnywhere, mais peut facilement être adaptée pour d'autres plateformes comme Heroku, AWS ou DigitalOcean.

### Configuration pour PythonAnywhere

```python
# wsgi.py
import os
import sys

# Chemin vers votre projet Django
path = '/home/theoldfox/fox-api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'FoxAPI.settings'

# Variables d'environnement pour la production
os.environ['ENV'] = 'production'
os.environ['DEBUG'] = 'False'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Configuration des fichiers statiques et médias

```python
# settings.py (extrait)

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuration Whitenoise pour les fichiers statiques
MIDDLEWARE = [
    # ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Sécurité en production

```python
# settings.py (extrait pour production)

DEBUG = False
ALLOWED_HOSTS = ['theoldfox.pythonanywhere.com', 'api.fox-dev.com']

# Protection CSRF
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Configuration CORS stricte
CORS_ALLOWED_ORIGINS = [
    'https://fox-dev.com',
    'https://www.fox-dev.com'
]

# En-têtes de sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
```

## 📝 Structure des articles

Les articles de blog (Post) ont une structure spécifique qu'il est crucial de comprendre pour l'implémentation frontend. **Le champ contenuP1 contient l'intégralité du contenu HTML formaté de l'article ce n'est pas forcement bootstrap ca pourait etre tailwind donc prevoir cela pour cette page de detail article**.

### Exemple de contenu d'article

Voici un exemple de contenu dans le champ `contenuP1` pour un article sur le projet FoxyBlueLight:

```html
<div class="container my-4" style="max-width: 950px;">
    <div class="bg-dark text-light p-3 p-md-4 rounded-3 shadow-lg" style="--bs-bg-opacity: .9; background-color: #1c1c1c !important; border: 1px solid #333;">

        <!-- Alerte Lancement / Soutien -->
        <div class="alert alert-dismissible fade show p-3 text-center rounded-3 mb-4" role="alert" style="background-color: #212121; border-left: 5px solid #ff8000; color: #f0f0f0;">
            <strong style="color: #ff8000; font-size: 1.2em;">🦊 J'ai pété le filtre lumière bleue de Windows ! 🦊</strong><br>
            <span class="fw-bold" style="color: #ffffff;">FoxyBlueLight</span> est maintenant disponible gratuitement pour tous les accros des écrans qui veulent garder leurs yeux en bon état !<br>
            <small class="text-muted" style="color: #cccccc !important;">PS : Oui, j'ai dû tout apprendre de zéro, et c'était chaud sa mère !!!! mais fallait le faire C# parce que c'est le mieux pour une app windows 🥵</small>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <!-- Bannière -->
        <div class="text-center mb-4">
            <img src="https://github.com/Tiger-Foxx/BlueLightFox/raw/main/FoxyBlueLight/Resources/logo.png" alt="Logo FoxyBlueLight" class="img-fluid rounded-3 shadow-sm mb-2" style="max-height: 250px; object-fit: contain; border: 1px solid #ff8000;">
            <div class="fst-italic text-muted" style="font-size: 0.9em; color: #cccccc !important;">
                "Parce que le filtre de Windows, c'est comme mettre des lunettes de soleil à 1€ pour aller sur la Lune."
            </div>
            <div class="mt-3">
                <a href="https://foxy-blue-light.the-fox.tech/" target="_blank" rel="noopener noreferrer" class="btn btn-sm fw-bold me-2 mb-2" style="background-color: #c6905f; color: #ffffff;">Télécharger l'application</a>
                <a href="https://github.com/Tiger-Foxx/BlueLightFox" target="_blank" rel="noopener noreferrer" class="btn btn-sm fw-bold mb-2" style="background-color: #ff8000; color: #ffffff;">Voir le projet sur GitHub</a>
            </div>
        </div>

        <!-- Titre -->
        <h1 class="text-center fw-bold border-bottom border-3 pb-3 mb-4" style="color: #ffffff; border-color: #ff8000 !important; font-size: 1.4rem;">
            Windows a un Filtre Lumière Bleue... Et J'ai Décidé de Lui Donner des Stéroïdes !
            <span class="d-block fw-normal mt-2" style="font-size: 1.1rem; color: #ff8000;">🦊 FoxyBlueLight : Comment j'ai tué mes nuits blanches (et appris C#) pour sauver vos yeux</span>
        </h1>

        <!-- Intro pour tous -->
        <div class="p-4 rounded-3 mb-4" style="background-color: #212121; border-left: 5px solid #ff8000; line-height: 1.7;">
            <h2 class="mt-0 fw-bold mb-3" style="color: #ffffff; font-size: 1.5rem;">Quand Windows te propose un couteau et que tu veux une épée laser...</h2>
            <p>
                Salut la team des yeux fatigués ! 👋 Un jour, après ma 37ème heure d'écran consécutive, j'ai décidé d'activer le fameux "mode nuit" de Windows. La grande révélation : c'est aussi basique qu'un tutorial "Hello World" ! Un seul curseur ? Pas de personnalisation ? Sérieusement, Microsoft ?!
            </p>
            <p>
                Frustré comme un développeur devant un bug inexplicable, j'ai décidé de créer <strong style="color: #ff8000;">FoxyBlueLight</strong>. Le petit hic ? Je n'avais JAMAIS codé en C# de ma vie. Mais bon, ça ne devait pas être si compliqué, non ? <i>(Narrateur : C'était en fait très compliqué)</i>
            </p>
            <div class="alert p-2 rounded" style="background-color: #2d2d2d;">
                <div class="d-flex">
                    <div class="flex-shrink-0">
                        <img src="https://avatars.githubusercontent.com/u/118616410?v=4" alt="Fox Avatar" width="50" height="50" class="rounded-circle" style="border: 2px solid #ff8000;">
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <p class="mb-0 fst-italic" style="color: #cccccc;">
                            "J'ai cru que j'allais devenir aveugle avant de finir cette app contre la fatigue oculaire. L'ironie, quoi !"
                            <span style="color: #ff8000;">— Moi-même, à 3h du matin, 47 erreurs de compilation plus tard</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Suite de l'article avec plus de contenu, images, code, etc. -->
    </div>
</div>
```

### Implications pour le frontend

Le frontend doit être conçu pour:

1. **Injecter directement le HTML** - Utiliser `dangerouslySetInnerHTML` en React ou `v-html` en Vue.js pour afficher le contenu:

```jsx
// Exemple React
function PostContent({ post }) {
  return (
    <div className="post-content">
      <div dangerouslySetInnerHTML={{ __html: post.contenuP1 }} />
    </div>
  );
}
```

2. **Gérer les styles CSS** - Les articles utilisent généralement Bootstrap et des styles inline, mais le frontend doit s'assurer que:
   - Les styles ne sont pas en conflit avec le design global
   - Les éléments responsifs fonctionnent correctement
   - Le thème sombre/clair est respecté

3. **Créer un conteneur flexible** - Créer un conteneur qui s'adapte aux différentes structures d'articles:

```jsx
// Approche conteneur flexible
function PostContainer({ post }) {
  return (
    <article className="article-container">
      <header className="article-header">
        <h1>{post.titre}</h1>
        <div className="article-meta">
          <span className="article-date">{formatDate(post.date)}</span>
          <span className="article-author">{post.auteur}</span>
          <span className="article-category">{post.categorie}</span>
        </div>
      </header>
      
      <figure className="article-featured-image">
        <img src={post.photo800_x_533} alt={post.titre} />
      </figure>
      
      <div className="article-content-wrapper">
        {/* Le contenu HTML complet de l'article */}
        <div dangerouslySetInnerHTML={{ __html: post.contenuP1 }} />
      </div>
      
      <footer className="article-footer">
        {/* Boutons de partage, tags, etc. */}
      </footer>
    </article>
  );
}
```

4. **Exemples visuels variés** - Les articles peuvent suivre différentes structures visuelles, le frontend doit être flexible.

## 🕰 Timeline interactive

La timeline est un élément clé qui présente le parcours professionnel et doit être implémentée avec une attention particulière aux détails visuels et animations.

### Données de la timeline

Le modèle Timeline contient des entrées chronologiques avec:
- `titre` - Nom de l'expérience ou formation
- `periode` - Période temporelle (ex: "2023-2024")
- `description` - Description détaillée
- `ordre` - Position dans la timeline (1 étant le plus récent)

### Exemples d'implémentation créative

La timeline doit être implémentée de manière exceptionnelle et créative. Voici quelques approches possibles:

#### 1. Timeline verticale avec animations au scroll

```jsx
// Exemple avec Framer Motion et animation au scroll
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

const TimelineItem = ({ item, index }) => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.2,
  });

  const variants = {
    hidden: { opacity: 0, x: index % 2 === 0 ? -50 : 50 },
    visible: { opacity: 1, x: 0 }
  };

  return (
    <motion.div
      ref={ref}
      className={`timeline-item ${index % 2 === 0 ? 'left' : 'right'}`}
      initial="hidden"
      animate={inView ? "visible" : "hidden"}
      variants={variants}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <div className="timeline-content">
        <div className="timeline-date">{item.periode}</div>
        <h3 className="timeline-title">{item.titre}</h3>
        <p className="timeline-description">{item.description}</p>
      </div>
    </motion.div>
  );
};

const Timeline = ({ items }) => {
  // Trier par ordre
  const sortedItems = [...items].sort((a, b) => a.ordre - b.ordre);
  
  return (
    <div className="timeline-container">
      <div className="timeline-line"></div>
      {sortedItems.map((item, index) => (
        <TimelineItem key={item.id} item={item} index={index} />
      ))}
    </div>
  );
};
```

#### 2. Timeline horizontale interactive avec Lottie

```jsx
// Exemple avec timeline horizontale et Lottie
import { useState } from 'react';
import Lottie from 'lottie-react';
import foxAnimation from '../assets/animations/fox-running.json';

const TimelineHorizontal = ({ items }) => {
  const [activeIndex, setActiveIndex] = useState(0);
  const sortedItems = [...items].sort((a, b) => a.ordre - b.ordre);
  
  return (
    <div className="timeline-horizontal">
      <div className="timeline-track">
        {sortedItems.map((item, index) => (
          <div 
            key={item.id}
            className={`timeline-node ${index === activeIndex ? 'active' : ''}`}
            onClick={() => setActiveIndex(index)}
          >
            <div className="timeline-dot"></div>
            <div className="timeline-year">{item.periode}</div>
          </div>
        ))}
        
        {/* Fox animation suivant la progression */}
        <div 
          className="fox-animation" 
          style={{ left: `calc(${(activeIndex / (sortedItems.length - 1)) * 100}% - 25px)` }}
        >
          <Lottie 
            animationData={foxAnimation} 
            style={{ width: 50, height: 50 }}
            loop={true}
          />
        </div>
      </div>
      
      <div className="timeline-content-display">
        {sortedItems[activeIndex] && (
          <div className="timeline-active-content">
            <h3>{sortedItems[activeIndex].titre}</h3>
            <p>{sortedItems[activeIndex].description}</p>
          </div>
        )}
      </div>
    </div>
  );
};
```

#### 3. Timeline 3D avec parallaxe

```jsx
// Concept de timeline 3D avec ThreeJS/react-three-fiber
import { Canvas } from '@react-three/fiber';
import { Text, Image, useScroll } from '@react-three/drei';
import { useRef } from 'react';

const TimelineItem3D = ({ item, index, position }) => {
  return (
    <group position={position}>
      <Text position={[0, 0.5, 0]} fontSize={0.2}>
        {item.titre}
      </Text>
      <Text position={[0, 0.2, 0]} fontSize={0.1} color="#FDE047">
        {item.periode}
      </Text>
      <Text position={[0, -0.1, 0]} fontSize={0.08} maxWidth={2}>
        {item.description}
      </Text>
    </group>
  );
};

const Timeline3D = ({ items }) => {
  const scrollRef = useRef();
  const sortedItems = [...items].sort((a, b) => a.ordre - b.ordre);
  
  return (
    <div className="timeline-3d-container" style={{ height: '100vh' }}>
      <Canvas>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        
        <group ref={scrollRef}>
          {sortedItems.map((item, index) => (
            <TimelineItem3D 
              key={item.id} 
              item={item} 
              index={index}
              position={[0, -index * 2, 0]}
            />
          ))}
        </group>
        
        <useScroll scrollRef={scrollRef} />
      </Canvas>
    </div>
  );
};
```

### Exploration créative

Le frontend est encouragé à explorer des approches créatives pour la timeline, comme:

- **Visualisations métaphoriques** - Représenter le parcours comme un chemin, une constellation, etc.
- **Interactions physiques** - Utiliser la physique (ressorts, gravité) pour les animations
- **Narration guidée** - Guide "Fox" accompagnant l'utilisateur dans le parcours
- **Parallaxe et profondeur** - Créer une sensation de profondeur avec des couches parallaxe
- **Transitions fluides** - Animations fluides entre les éléments de la timeline

## 💼 Attentes frontend

Le frontend React qui consommera cette API doit offrir une expérience utilisateur exceptionnelle, à la hauteur de la qualité de l'API. Voici les directives et attentes pour le développement frontend.

### 🎨 Identité visuelle et design

La plateforme doit refléter l'identité "Fox" avec un design sombre et élégant rehaussé d'accents orange/jaune:

- **Palette principale**:
  - Noir profond: `#0F172A` (fond)
  - Gris foncé: `#1E293B` (éléments d'interface, cartes)
  - Gris clair: `#E2E8F0` (texte principal)
  - Orange/Jaune: `#FDE047` (accents, boutons, liens)

- **Typographie**:
  - Titres: SF Pro Display, Roboto ou équivalent sans-serif
  - Corps: Inter, Open Sans ou équivalent lisible
  - Hiérarchie claire avec variation de taille et graisse

- **Iconographie**:
  - Style minimaliste et cohérent
  - Set d'icônes comme Phosphor, Feather ou Heroicons
  - Utilisation judicieuse (ne pas surcharger)

### 🧩 Structure et composants

#### Structure globale

```jsx
// Structure d'application proposée
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import { Navbar, Footer, ScrollToTop } from './components/layout';
import { Home, Projects, Blog, Post, Contact, About, Admin } from './pages';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <ScrollToTop />
          <Navbar />
          <main className="min-h-screen">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/blog" element={<Blog />} />
              <Route path="/blog/:id" element={<Post />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/about" element={<About />} />
              <Route path="/admin/*" element={<Admin />} />
            </Routes>
          </main>
          <Footer />
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
```

#### Composants clés à développer

**Navigation avancée**:
- Barre de navigation réactive avec transitions fluides
- Menu mobile avec animations élégantes
- Indicateur de page active
- Transitions entre pages

**Sections d'accueil**:
- Hero section avec animations subtiles
- Showcase de projets avec effets de survol
- Timeline interactive et animée
- Témoignages en carousel dynamique
- Appels à l'action flottants

**Cartes de projet**:
- Effets de profondeur et d'élévation
- Transitions au survol
- Vignettes avec informations partielles
- Modal détaillé ou page dédiée

**Blog interactif**:
- Maquette d'article avec typographie soignée
- Système de commentaires intégré
- Partage sur réseaux sociaux
- Tags et filtres dynamiques

**Formulaires élégants**:
- Validation interactive
- Animations de transition
- États de chargement et de succès
- Messages d'erreur contextuels

**Tableau de bord admin**:
- Interface sécurisée avec authentification
- Statistiques visuelles
- Gestion de contenu intuitive
- Prévisualisations en direct

### 🧠 Approche technique

```jsx
// Exemple d'un hook personnalisé pour les appels API
import { useState, useEffect } from 'react';
import axios from 'axios';

export const useApi = (endpoint, initialData = null) => {
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const baseUrl = 'https://api.fox-dev.com';

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${baseUrl}${endpoint}`);
      setData(response.data);
      setError(null);
    } catch (err) {
Pour finir correctement le README, voici la partie manquante et la conclusion :

```jsx
// Exemple d'un hook personnalisé pour les appels API (suite)
      console.error(`Erreur lors de la récupération de ${endpoint}:`, err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [endpoint]);

  const refetch = () => fetchData();

  return { data, loading, error, refetch };
};
```

### 🎭 Animations et interactions

Le frontend doit incorporer des animations soignées pour une expérience immersive:

- **Entrées de page** fluides avec mécanismes comme Framer Motion
- **Transitions entre vues** sans rupture
- **Animations au scroll** pour révéler les contenus progressivement
- **Parallaxe subtile** sur certains éléments visuels
- **Microinteractions** sur les éléments interactifs
- **Lottie animations** pour certains éléments clés (logo Fox, loader, illustrations)

```jsx
// Exemple de composant avec animation Framer Motion
import { motion } from 'framer-motion';

const ProjectCard = ({ project }) => {
  return (
    <motion.div
      className="card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ scale: 1.03, boxShadow: '0 10px 25px rgba(0,0,0,0.2)' }}
      transition={{ duration: 0.3 }}
    >
      <img src={project.photo1_800_x_550} alt={project.nom} />
      <div className="content">
        <h3>{project.nom}</h3>
        <p>{project.description}</p>
        <div className="tags">
          <span className="tag">{project.categorie}</span>
          {project.sujet && <span className="tag">{project.sujet}</span>}
        </div>
      </div>
    </motion.div>
  );
};
```

### 🌟 Fonctionnalités spéciales et liberté créative

Le frontend doit non seulement implémenter les fonctionnalités de base, mais aussi explorer des approches créatives et innovantes. Il ne s'agit pas simplement de suivre des directives rigides, mais d'apporter une vision artistique et technique qui démontre une vraie maîtrise du développement frontend.

#### Innovations et libertés encouragées

- **Au-delà des carousels standard** - Explorer des alternatives comme des galeries 3D, des sliders physiques (avec effets d'inertie), ou des transitions personnalisées.
- **Visualisations de données créatives** - Pour la section timeline, les statistiques ou les projets, privilégier des représentations visuelles uniques plutôt que des graphiques standards.
- **Interactions expérimentales** - Ne pas hésiter à implémenter des gestes de navigation non conventionnels mais intuitifs.
- **Effets visuels signatures** - Développer des effets visuels qui deviennent partie intégrante de l'identité du site.
- **Intégrations audio subtiles** - Considérer des retours sonores discrets pour certaines interactions importantes.

#### Mode dark/light avec préférence dark

```jsx
// Contexte de thème
import { createContext, useState, useEffect, useContext } from 'react';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(true); // Default to dark

  useEffect(() => {
    // Check user preference or saved setting
    const savedMode = localStorage.getItem('foxTheme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode) {
      setDarkMode(savedMode === 'dark');
    } else {
      setDarkMode(prefersDark);
    }
  }, []);

  const toggleTheme = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('foxTheme', newMode ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', newMode);
  };

  return (
    <ThemeContext.Provider value={{ darkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
```

#### Support multilingue (FR/EN)

```jsx
// Configuration i18n
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      fr: {
        translation: {
          welcome: 'Bienvenue chez Fox',
          projects: 'Projets',
          blog: 'Blog',
          contact: 'Contact',
          about: 'À propos',
          // Plus de traductions...
        }
      },
      en: {
        translation: {
          welcome: 'Welcome to Fox',
          projects: 'Projects',
          blog: 'Blog',
          contact: 'Contact',
          about: 'About',
          // Plus de traductions...
        }
      }
    },
    lng: 'fr', // Langue par défaut
    fallbackLng: 'fr',
    interpolation: {
      escapeValue: false
    }
  });
```

#### Tracking des visites

```jsx
// Service de tracking
export const trackPageView = async (page) => {
  try {
    const referrer = document.referrer || 'direct';
    await fetch('https://api.fox-dev.com/api/track-visitor/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        page,
        referrer
      }),
    });
  } catch (error) {
    console.error('Erreur de tracking:', error);
    // Non bloquant, continue silencieusement
  }
};

// Dans le composant App
useEffect(() => {
  return history.listen((location) => {
    trackPageView(location.pathname);
  });
}, [history]);
```

### 📱 Responsive design

Le design doit être exceptionnellement responsive avec une approche mobile-first:

- **Breakpoints** standards mais complets
- **Layouts fluides** s'adaptant à tous les écrans
- **Navigation mobile** intuitive (menu hamburger, swipe)
- **Images optimisées** pour chaque taille d'écran
- **Touch controls** sur mobile (swipe, pinch, etc.)
- **Performance optimisée** pour appareils bas de gamme

```jsx
// Exemple de composant responsive avec Tailwind CSS
const ProjectsGrid = ({ projects }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
      {projects.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
};
```

### 🛠️ Stack technologique recommandée

- **Vite.js** - Pour le bundling et le développement rapide
- **React 18+** - Pour l'interface utilisateur
- **Tailwind CSS** - Pour le styling efficace et responsive
- **Framer Motion** - Pour les animations fluides
- **React Router 6** - Pour la navigation
- **Axios** - Pour les appels API
- **React Query** - Pour la gestion des états serveur
- **Zustand/Context API** - Pour la gestion d'état
- **i18next** - Pour l'internationalisation
- **React Hook Form** - Pour les formulaires
- **Zod** - Pour la validation
- **Three.js/React Three Fiber** - Pour les éléments 3D (optionnel)
- **Lottie** - Pour les animations complexes

### 🧪 Méthodologie

- **Approche composants** - Architecture modulaire
- **Atomic Design** - Structuration par complexité
- **Mobile-first** - Concevoir pour mobile d'abord
- **Performance-driven** - Optimisation continuelle
- **Accessibilité** - WCAG 2.1 AA minimum
- **Tests** - Composants testés avec Vitest/Jest

## 👤 À propos de l'auteur

<div align="center">
  <img src="docs/images/arthur-donfack.jpg" alt="Arthur Donfack" width="200" style="border-radius: 50%"/>
  <h3>Arthur Donfack | Fox</h3>
  <p>Développeur & Hacker Éthique</p>
</div>

Étudiant en génie informatique à l'École Nationale Supérieure Polytechnique de Yaoundé (ENSPY), Arthur combine des compétences en développement web, mobile et en cybersécurité. Connu sous le pseudonyme "Fox" ou "The Tiger Fox", il se passionne pour les technologies innovantes et la sécurité des systèmes.

### Parcours professionnel (timeline)

- **2024-Présent** - ML & IA pour sécurité réseau
- **2023-2024** - Spécialisation en sécurité informatique
- **2024** - Spring Boot, JEE, frameworks JS frontend
- **2022-2023** - Développement Java avancé
- **2020-2021** - Développement mobile Flutter
- **2019-2020** - Django et développement web
- **2018-2019** - Python avancé

### Contact

- **Email**: donfackarthur750@gmail.com
- **WhatsApp**: +237 658 866 639
- **Localisation**: École Polytechnique – Yaoundé, Melen
- **GitHub**: [theTigerFox](https://github.com/theTigerFox)

### Philosophie

> "Le débogage, c'est comme être détective dans un film où tu es aussi le criminel."

## 📚 Ressources et liens

- [Documentation Django REST Framework](https://www.django-rest-framework.org/)
- [Django Project](https://www.djangoproject.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)
- [Vite.js](https://vitejs.dev/guide/)
- [Lottie Files](https://lottiefiles.com/) - Pour les animations
- [Unsplash](https://unsplash.com/) - Images libres de droits
- [Heroicons](https://heroicons.com/) - Set d'icônes
- [Dribbble](https://dribbble.com/) - Inspiration design

## 🔮 Perspectives d'évolution

Le projet a été conçu avec l'évolutivité en tête. Parmi les développements futurs envisagés :

- **API GraphQL** - Alternative à l'API REST pour des requêtes plus flexibles
- **Application mobile native** - Version React Native pour iOS/Android
- **Système de cours en ligne** - Extension pour proposer des formations
- **Espace client** - Portail sécurisé pour les clients avec suivi de projet
- **Blog multiauteur** - Possibilité d'inviter d'autres experts à contribuer
- **Intégration IA** - Chatbot et recommandations personnalisées

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">
  <p>Fox, life is easier : The genius at the disposal of all your dreams.</p>
  <p>© 2025 Fox. Tous droits réservés.</p>
</div>      