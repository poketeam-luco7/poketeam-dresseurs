FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
# Applique les migrations puis démarre le serveur de production
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi -b 0.0.0.0:8001 -w 2"]
