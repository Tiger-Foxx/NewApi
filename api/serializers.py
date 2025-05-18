from rest_framework import serializers
from .models import (
    Profile, Project, Post, Visiteur, Commentaire, 
    Message, Annonce, Newsletter, Timeline, Temoignage
)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class VisiteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visiteur
        fields = '__all__'

class CommentaireSerializer(serializers.ModelSerializer):
    visiteur_email = serializers.ReadOnlyField(source='visiteur.email')
    visiteur_nom = serializers.ReadOnlyField(source='visiteur.nom')
    
    class Meta:
        model = Commentaire
        fields = '__all__'
        extra_fields = ['visiteur_email', 'visiteur_nom']

class MessageSerializer(serializers.ModelSerializer):
    visiteur_email = serializers.ReadOnlyField(source='visiteur.email')
    
    class Meta:
        model = Message
        fields = '__all__'
        extra_fields = ['visiteur_email']

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'

class TemoignageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temoignage
        fields = '__all__'

# Serializer spécial pour les inscriptions à la newsletter
class SubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    nom = serializers.CharField(max_length=100, required=False, allow_blank=True)