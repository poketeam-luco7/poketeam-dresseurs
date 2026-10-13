from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    mail = serializers.EmailField()
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    mdp = serializers.CharField(min_length=6, write_only=True)
    photoProfil = serializers.CharField(max_length=255, required=False)


class LoginSerializer(serializers.Serializer):
    mail = serializers.EmailField()
    mdp = serializers.CharField()


class UpdateSerializer(serializers.Serializer):
    """Tous les champs sont optionnels : on ne modifie que ce qui est envoyé."""
    mail = serializers.EmailField(required=False)
    nom = serializers.CharField(max_length=100, required=False)
    prenom = serializers.CharField(max_length=100, required=False)
    photoProfil = serializers.CharField(max_length=255, required=False)
    mdp = serializers.CharField(min_length=6, required=False, allow_blank=True)
