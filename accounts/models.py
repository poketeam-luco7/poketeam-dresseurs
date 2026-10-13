from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Dresseur(models.Model):
    """Reprend UserEntity du monolithe, sans la relation vers les équipes :
    les équipes vivent dans un autre service, qui ne garde que l'id du dresseur."""

    mail = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    photo_profil = models.CharField(max_length=255, default="/img/pokeball.png")
    password = models.CharField(max_length=128)  # haché, jamais en clair
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw):
        self.password = make_password(raw)

    def check_password(self, raw):
        return check_password(raw, self.password)

    def public(self):
        """Format attendu par le front (mêmes clés que l'ancien monolithe)."""
        return {
            "id": self.id,
            "mail": self.mail,
            "nom": self.nom,
            "prenom": self.prenom,
            "photoprofil": self.photo_profil,
        }
