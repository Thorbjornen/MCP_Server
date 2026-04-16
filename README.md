# MCP Server

## Architecture

Le projet repose sur l'architecture **Hôte-Client-Serveur** du protocole MCP :
- **Serveur** (`weather_server.py`) : Expose des outils (Tools) et des ressources (Resources) via `FastMCP`.
- **Client** (`client_test.py`) : Un agent intelligent (`smolagents`) qui consomme les outils du serveur pour répondre à des requêtes complexes.
- **Protocole** : Communication via l'entrée/sortie standard (STDIO).

## Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-utilisateur/mcp-weather-server.git
   cd mcp-weather-server
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

##️ Configuration

Créez un fichier `.env` à la racine du projet et ajoutez vos clés API :

```env
HF_TOKEN=votre_token_hugging_face
GOOGLE_API_KEY=votre_cle_api_google (optionnel)
```

> **Note** : Le fichier `.env` est ignoré par Git pour des raisons de sécurité (voir `.gitignore`).

## Utilisation

### 1. Démarrer l'Agent de test
Vous n'avez pas besoin de lancer le serveur manuellement. Le client s'en charge automatiquement au lancement :

```bash
python client_test.py
```

### 2. Fonctionnalités disponibles
- **Outils (Tools)** :
    - `get_available_cities` : Liste des villes gérées.
    - `get_weather` : Météo actuelle (température, humidité, conditions).
    - `calculate_travel_time` : Estimation du temps de trajet entre deux villes.
    - `get_city_comparison` : Comparaison thermique entre deux destinations.
- **Ressources (Resources)** :
    - `stats://tool-usage` : Statistiques dynamiques d'utilisation des outils.

## Contenu du Projet

- `weather_server.py` : Logique du serveur MCP (FastMCP).
- `client_test.py` : Scripts de test (Inspection et Agent Hugging Face).
- `TP_MCP_Etudiants.ipynb` : Notebook original du TP pour l'exploration.
- `requirements.txt` : Liste des bibliothèques Python nécessaires.
- `.gitignore` : Protection des fichiers sensibles et temporaires.

## Ressources
- [Documentation Officielle MCP](https://modelcontextprotocol.io/)
- [SDK Python MCP](https://github.com/modelcontextprotocol/python-sdk)
- [Hugging Face smolagents](https://huggingface.co/docs/smolagents)