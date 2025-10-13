# 🏥 HealthCare App

![CI/CD](https://github.com/slimbentanfous/HealthCare-app/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/slimbentanfous/HealthCare-app/branch/master/graph/badge.svg)](https://codecov.io/gh/slimbentanfous/HealthCare-app)
![Docker Pulls](https://img.shields.io/docker/pulls/slimbentanfous1/healthcare-app)
![Python](https://img.shields.io/badge/python-3.11-blue)

## 📌 Description
**HealthCare App** est une API REST sécurisée permettant de gérer :
- 🔐 Authentification avec JWT  
- 👩‍⚕️ Gestion des patients  
- 📅 Gestion des rendez-vous  
- 🛡️ Tests unitaires avec `pytest` + couverture envoyée sur **Codecov**  
- 🐳 Déploiement containerisé via **Docker Hub**

---

## ⚙️ Stack Technique
- **Backend** : Flask (Python 3.11)  
- **Database** : PostgreSQL  
- **Auth** : JWT (flask-jwt-extended)  
- **CI/CD** : GitHub Actions + Codecov + Docker Hub  

---

## 🚀 Installation & Lancement

### 1️⃣ Cloner le repo
```bash
git clone https://github.com/slimbentanfous/HealthCare-app.git
cd HealthCare-app
```

### 2️⃣ Lancer avec Docker
```bash
docker-compose up -d --build
```

API disponible sur :  
👉 `http://localhost:5000`

---

## 🧪 Tests
Exécuter les tests avec couverture :
```bash
docker-compose exec api pytest --cov=. --cov-report=term
```

---

## 📦 Docker Hub
Images disponibles ici :  
🔗 [Docker Hub - slimbentanfous1/healthcare-app](https://hub.docker.com/r/slimbentanfous1/healthcare-app)

```bash
# Dernière version
docker pull slimbentanfous1/healthcare-app:latest

# Version spécifique
docker pull slimbentanfous1/healthcare-app:1.0.0
```

---

## 🛠 Endpoints Principaux

- `POST /auth/register` → Créer un compte  
- `POST /auth/login` → Connexion (JWT)  
- `GET /patients/` → Liste des patients  
- `POST /patients/` → Créer un patient  
- `GET /appointments/` → Liste des rendez-vous  
- `POST /appointments/` → Créer un rendez-vous  

---

## ✨ Badges
- ✅ Tests automatisés avec GitHub Actions  
- 📊 Couverture Codecov  
- 🐳 Image disponible sur Docker Hub  

---

## 👨‍💻 Auteur
Projet développé par **Slim Ben Tanfous**  
🔗 [LinkedIn](https://www.linkedin.com/in/slim-ben-tanfous-971b19244/) | 🔗 [GitHub](https://github.com/slimbentanfous)
