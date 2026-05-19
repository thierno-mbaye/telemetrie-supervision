# 📡 Système de supervision de télémétrie

Plateforme open-source de collecte, stockage, alerting et visualisation de métriques multi-domaines — infrastructure IT, IoT industriel et microservices applicatifs.

---

## 🏗️ Architecture

Capteurs IoT (MQTT) → Mosquitto → Telegraf → Prometheus → Grafana
VM Linux (métriques) → Node Exporter → Prometheus → Grafana
Conteneurs Docker → cAdvisor → Prometheus → Grafana
Microservice FastAPI → /metrics → Prometheus → Grafana
                                    └→ Alertmanager → Notifications

---

## 🧱 Stack technique

- Prometheus 2.54 — Scraping des métriques, stockage TSDB
- Alertmanager 0.27 — Routage et déduplication des alertes
- Grafana 11.2 — Dashboards provisionnés automatiquement
- Telegraf 1.32 — Bridge MQTT vers Prometheus
- Eclipse Mosquitto 2.0 — Broker MQTT pour les capteurs IoT
- Docker Compose v2 — Déploiement reproductible
- Python 3.12 + FastAPI — Microservice instrumenté méthode RED

---

## 🚀 Démarrage rapide

Prérequis : Docker Engine 24+ et Docker Compose v2

    git clone https://github.com/thierno-mbaye/telemetrie-supervision
    cd telemetrie-supervision
    docker compose up --build -d

---

## 🌐 Accès aux interfaces

- Grafana      : http://localhost:3000  (admin / admin123)
- Prometheus   : http://localhost:9090
- Alertmanager : http://localhost:9093
- Pushgateway  : http://localhost:9091
- Microservice : http://localhost:8000

---

## 📊 Dashboards Grafana

Infrastructure :
- CPU Usage % en temps réel
- RAM disponible %
- Status UP/DOWN de tous les services

IoT — Supervision capteurs :
- Température par capteur (°C)
- Niveau batterie (%) avec décharge progressive
- Vibration avec détection de pics
- Pression atmosphérique (hPa)

---

## 🚨 Règles d'alerting (8 règles actives)

Domaine Infra :
- CPUElevé         : CPU > 80% pendant 2min     [warning]
- MémoireInsuffisante : RAM < 15% pendant 2min  [critical]
- DisquePresquePlein  : Disque < 20% pdt 5min   [warning]
- ServiceDown      : Service injoignable 1min    [critical]

Domaine IoT :
- TempératureCritique : Temp > 40°C pendant 1min   [critical]
- BatterieFaible      : Batterie < 20% pdt 2min     [warning]

Domaine Applicatif :
- TauxErreurÉlevé : Erreurs 5xx > 5% pendant 2min  [critical]
- LatenceÉlevée   : p95 > 1s pendant 2min           [warning]

---

## 🌐 Simulateur IoT

3 capteurs simulés : salle-serveurs, datacenter, atelier-iot
Données : température, pression, vibration, batterie

---

## 📁 Structure du projet

telemetrie/
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml
│   └── rules.yml
├── alertmanager/
│   └── alertmanager.yml
├── grafana/
│   └── provisioning/
├── mosquitto/
│   └── mosquitto.conf
├── telegraf/
│   └── telegraf.conf
└── microservice/
    ├── main.py
    ├── simulator.py
    ├── requirements.txt
    └── Dockerfile

---

## 👨‍💻 Auteur

Thierno Mbaye — Étudiant Mastère Expert IT — Cybersécurité et Réseaux
Portfolio : https://thierno-mbaye.github.io
LinkedIn  : https://linkedin.com/in/thierno-mbaye
