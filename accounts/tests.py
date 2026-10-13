import jwt
from django.conf import settings
from rest_framework.test import APITestCase

from .models import Dresseur

SACHA = {"mail": "sacha@bourg-palette.fr", "nom": "Ketchum", "prenom": "Sacha",
         "mdp": "pikapika", "photoProfil": "/img/masterball.png"}


class DresseursTests(APITestCase):
    def register(self, **extra):
        return self.client.post("/users", {**SACHA, **extra}, format="json")

    def login(self, mdp="pikapika"):
        return self.client.post("/auth/login", {"mail": SACHA["mail"], "mdp": mdp}, format="json")

    def test_inscription_hache_le_mot_de_passe(self):
        r = self.register()
        self.assertEqual(r.status_code, 201)
        self.assertNotIn("mdp", r.json())
        d = Dresseur.objects.get(mail=SACHA["mail"])
        self.assertNotEqual(d.password, "pikapika")  # plus jamais en clair
        self.assertTrue(d.check_password("pikapika"))

    def test_inscription_mail_deja_pris(self):
        self.register()
        self.assertEqual(self.register(mail=SACHA["mail"].upper()).status_code, 409)

    def test_inscription_invalide(self):
        self.assertEqual(self.register(mdp="123").status_code, 400)

    def test_login_renvoie_le_format_du_front(self):
        self.register()
        r = self.login()
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertEqual(body["user"]["photoprofil"], "/img/masterball.png")
        payload = jwt.decode(body["accessToken"], settings.JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(payload["sub"], str(body["user"]["id"]))

    def test_login_mauvais_mot_de_passe(self):
        self.register()
        self.assertEqual(self.login("mauvais").status_code, 401)

    def test_profil_via_en_tete_gateway(self):
        uid = self.register().json()["id"]
        self.assertEqual(self.client.get("/auth/profile").status_code, 401)
        r = self.client.get("/auth/profile", HTTP_X_USER_ID=str(uid))
        self.assertEqual(r.json()["prenom"], "Sacha")

    def test_modification_de_son_profil_uniquement(self):
        uid = self.register().json()["id"]
        self.assertEqual(self.client.put("/users", {"nom": "Pirate"}, format="json").status_code, 401)
        r = self.client.put("/users", {"nom": "Ketchum-Chen", "mdp": ""}, format="json",
                            HTTP_X_USER_ID=str(uid))
        self.assertEqual(r.json()["nom"], "Ketchum-Chen")
        self.assertEqual(self.login().status_code, 200)  # mdp vide = inchangé
