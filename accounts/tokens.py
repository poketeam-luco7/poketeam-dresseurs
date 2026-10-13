from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings


def create_token(dresseur) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(dresseur.id),  # la gateway en fait l'en-tête X-User-Id
        **dresseur.public(),
        "iat": now,
        "exp": now + timedelta(minutes=settings.JWT_EXPIRES_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
