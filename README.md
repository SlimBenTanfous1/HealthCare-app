# 🏥 HealthCare App

![CI/CD](https://github.com/slimbentanfous1/HealthCare-app/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/slimbentanfous1/HealthCare-app/branch/master/graph/badge.svg)](https://codecov.io/gh/slimbentanfous1/HealthCare-app)
![Docker Pulls](https://img.shields.io/docker/pulls/slimbentanfous1/healthcare-app)

Une application **Flask + PostgreSQL + JWT** pour la gestion des patients et des rendez-vous, avec un pipeline CI/CD complet.

---

## 🚀 Fonctionnalités

- Authentification avec **JWT**
- CRUD **Patients**
- CRUD **Appointments**
- Tests unitaires avec **Pytest**
- Couverture de code via **Codecov**
- Build et push Docker automatique
- Versioning automatique avec Git tags

---

## 📦 Installation locale

### 1. Cloner le projet
```bash
git clone https://github.com/slimbentanfous1/HealthCare-app.git
cd HealthCare-app
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
flask run
```
➡️ API dispo sur [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🐳 Installation avec Docker

```bash
docker-compose up --build
```

➡️ API dispo sur [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ✅ Tests

Lancer les tests avec couverture :
```bash
pytest --cov=. --cov-report=term
```

---

## 🔗 Endpoints principaux

### Auth
- `POST /auth/register` → Inscription
- `POST /auth/login` → Connexion

### Patients
- `GET /patients/` → Liste des patients
- `POST /patients/` → Ajouter un patient
- `GET /patients/<id>` → Récupérer un patient

### Appointments
- `GET /appointments/` → Liste des rendez-vous
- `POST /appointments/` → Ajouter un rendez-vous
- `DELETE /appointments/<id>` → Supprimer un rendez-vous

---

## 📊 CI/CD

- **GitHub Actions** : build, test, coverage, version bump, push Docker image
- **Codecov** : suivi de la couverture
- **DockerHub** : image disponible sous `slimbentanfous1/healthcare-app`

---

## 🛡️ Améliorations futures

- Ajouter **Swagger/OpenAPI** pour documentation auto
- Déploiement auto (Heroku / Render / Fly.io)
- Ajout lint & format (Black, Flake8, mypy)
- Observabilité (logs, métriques, monitoring)

---
