from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dresseur
from .serializers import LoginSerializer, RegisterSerializer, UpdateSerializer
from .tokens import create_token


def current_dresseur(request):
    """La gateway a vérifié le JWT et transmis l'id dans X-User-Id."""
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return None
    return Dresseur.objects.filter(pk=user_id).first()


def unauthorized():
    return Response({"error": "Non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)


class UsersView(APIView):
    def post(self, request):
        """Inscription (publique)."""
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        data = s.validated_data
        if Dresseur.objects.filter(mail__iexact=data["mail"]).exists():
            return Response({"error": "Adresse mail déjà utilisée"}, status=status.HTTP_409_CONFLICT)

        d = Dresseur(mail=data["mail"].lower(), nom=data["nom"], prenom=data["prenom"])
        if data.get("photoProfil"):
            d.photo_profil = data["photoProfil"]
        d.set_password(data["mdp"])
        d.save()
        return Response(d.public(), status=status.HTTP_201_CREATED)

    def put(self, request):
        """Modification du profil : uniquement le sien (corrige la faille du monolithe)."""
        d = current_dresseur(request)
        if d is None:
            return unauthorized()
        s = UpdateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        data = s.validated_data

        new_mail = data.get("mail", d.mail).lower()
        if new_mail != d.mail and Dresseur.objects.filter(mail__iexact=new_mail).exists():
            return Response({"error": "Adresse mail déjà utilisée"}, status=status.HTTP_409_CONFLICT)
        d.mail = new_mail
        d.nom = data.get("nom", d.nom)
        d.prenom = data.get("prenom", d.prenom)
        d.photo_profil = data.get("photoProfil", d.photo_profil)
        if data.get("mdp"):  # mot de passe vide = inchangé
            d.set_password(data["mdp"])
        d.save()
        return Response(d.public())


class LoginView(APIView):
    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = Dresseur.objects.filter(mail__iexact=s.validated_data["mail"]).first()
        if d is None or not d.check_password(s.validated_data["mdp"]):
            return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"accessToken": create_token(d), "user": d.public()})


class ProfileView(APIView):
    def get(self, request):
        d = current_dresseur(request)
        if d is None:
            return unauthorized()
        return Response(d.public())


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})
