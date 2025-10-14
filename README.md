# 🏥 Healthcare App  

[![CI/CD](https://github.com/slimbentanfous1/HealthCare-app/actions/workflows/ci.yml/badge.svg)](https://github.com/slimbentanfous1/HealthCare-app/actions)  
[![codecov](https://codecov.io/gh/slimbentanfous1/HealthCare-app/branch/master/graph/badge.svg)](https://codecov.io/gh/slimbentanfous1/HealthCare-app)  
[![Docker](https://img.shields.io/docker/pulls/slimbentanfous1/healthcare-app)](https://hub.docker.com/r/slimbentanfous1/healthcare-app)  
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  

Une application web moderne de gestion **patients** et **rendez-vous médicaux**, construite avec **Flask + PostgreSQL + JWT + Swagger + Docker**.  

---

## ✨ Fonctionnalités

- 🔐 **Authentification JWT** (Register / Login sécurisés)  
- 👩‍⚕️ **Gestion des patients** : CRUD complet (ajout, lecture, suppression)  
- 📅 **Gestion des rendez-vous** : planification et suivi des consultations  
- 📊 **Swagger UI** pour tester facilement l’API (`/apidocs`)  
- 🐳 **Docker + Docker Compose** (API, DB, pgAdmin)  
- ✅ **CI/CD GitHub Actions** avec tests unitaires (Pytest + Coverage + Codecov)  
- 🗄️ **pgAdmin 4** pour la gestion visuelle de la base PostgreSQL  

---

## 🛠️ Stack Technique

- **Backend** : Python 3.11, Flask, SQLAlchemy, Flask-Migrate, JWT, Flasgger  
- **Base de données** : PostgreSQL 15  
- **Admin DB** : pgAdmin 4 (port 5050)  
- **Tests** : Pytest + Coverage  
- **CI/CD** : GitHub Actions + Codecov  
- **Containerisation** : Docker, Docker Hub  

---

## 📂 Architecture du projet

```
HealthCare-app/
│── app.py                # Point d'entrée Flask
│── wsgi.py               # Pour Gunicorn
│── models.py             # Modèles SQLAlchemy
│── extensions.py         # Initialisation db/jwt/migrate
│── routes/               # Blueprints Flask
│    ├── auth.py
│    ├── patients.py
│    └── appointments.py
│── templates/            # Dashboard HTML (Bootstrap)
│── static/               # JS / CSS (frontend léger)
│── migrations/           # Alembic (Flask-Migrate)
│── tests/                # Pytest + fixtures
│── seed.py               # Script pour données de test
│── docker-compose.yml    # Orchestration containers
│── Dockerfile            # Build API
│── .env                  # Variables d’environnement
│── requirements.txt      # Dépendances Python
│── ci.yml                # Pipeline GitHub Actions
│── README.md             # Documentation
```

---

## ⚙️ Installation locale

```bash
git clone https://github.com/slimbentanfous1/HealthCare-app.git
cd HealthCare-app

# Créer un venv
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer migrations
flask db init
flask db migrate -m "init"
flask db upgrade

# Seed data (optionnel)
python seed.py

# Lancer serveur
flask run
```

➡️ Accéder à : [http://localhost:5000](http://localhost:5000)  

---

## 🐳 Utilisation avec Docker

```bash
# Lancer containers
docker-compose up --build

# Vérifier les services
docker ps

# API:        http://localhost:5000
# Swagger:    http://localhost:5000/apidocs
# pgAdmin:    http://localhost:5050 (user: admin@healthcare.com / pass: admin123)
```

---

## 🚀 CI/CD

- Chaque **push** sur `master` déclenche :  
  ✅ Installation des dépendances  
  ✅ Lancement des tests (`pytest --cov`)  
  ✅ Upload de la couverture sur Codecov  
  ✅ Build + push de l’image Docker sur Docker Hub  
  ✅ Tagging automatique basé sur le commit message (`#major`, `#minor`, `#patch`)  

---

## 📸 Screenshots

### Dashboard  
![dashboard](./docs/screens/dashboard.png)

### Swagger UI  
![swagger](./docs/screens/swagger.png)

---

## 📈 Exemple API

### Register
```http
POST /auth/register
{
  "username": "slim",
  "password": "test"
}
```

### Login
```http
POST /auth/login
→ Returns JWT token
```

### Add Patient
```http
POST /patients/
{
  "name": "Alice",
  "age": 25,
  "diagnosis": "Flu"
}
```

---

## ✅ TODO / Améliorations

- [ ] Ajouter **rôles utilisateurs** (admin/doctor/nurse)  
- [ ] Ajouter **upload de documents médicaux**  
- [ ] Intégrer **Grafana/Prometheus** pour la surveillance  
- [ ] Ajouter un **frontend React/Next.js**  

---

## 📜 License

Distribué sous licence **MIT**.  
© 2025 Slim Ben Tanfous.  
