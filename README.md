# PokéTeam — Dresseurs

Microservice des **comptes** (Django + DRF + PostgreSQL) : inscription, connexion, profil.
Il **signe** les JWT ; la gateway les vérifie.

| | |
|---|---|
| Stack | Python 3.12, Django 5.1, DRF, PyJWT |
| Base | PostgreSQL 16 (SQLite en développement hors Docker) |
| Port interne | 8001 |
| Appelé par | la gateway |

## Routes

| Méthode | Route | Rôle |
|---|---|---|
| POST | `/users` | Inscription |
| PUT | `/users` | Modifier son profil |
| POST | `/auth/login` | Connexion, renvoie `{ accessToken, user }` |
| GET | `/auth/profile` | Son profil |
| GET | `/health` | Santé |

L'identité de l'appelant arrive dans l'en-tête `X-User-Id`, posé par la gateway.

## Variables d'environnement

| Variable | Rôle |
|---|---|
| `JWT_SECRET` | Secret de signature des tokens (partagé avec la gateway) |
| `DJANGO_SECRET_KEY` | Clé Django |
| `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Base ; sans `POSTGRES_HOST`, SQLite local |

## Lancer seul

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

## Tests

```bash
python manage.py test        # 7 tests
```

Mots de passe hachés en PBKDF2 (le monolithe d'origine les stockait en clair).

## Fait partie de PokéTeam

Ce dépôt est un des composants de l'organisation [poketeam-luco7](https://github.com/poketeam-luco7).
Pour lancer l'application complète (gateway, 3 services, 2 bases), voir le dépôt
d'orchestration [`poketeam`](https://github.com/poketeam-luco7/poketeam) : `docker-compose.yml`,
architecture (C4) et décisions d'architecture (ADR).
