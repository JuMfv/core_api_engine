# 🚀 Core API Engine (TMDB & PokéAPI)

Projet d'ingénierie de données et moteur d'interaction API développé sous Google Colab.

## 🛠️ Architecture du Projet

1. **TMDB Engine (Mini-Projet 1)** :
   - Extraction des détails de films avec gestion des clés API et retry HTTP (Q1).
   - Ingestion des dumps `.json.gz` quotidiens et traitement JSON Lines.
   - Stockage dans une base de données relationnelle SQLite.
   - Automatique trimestrielle des données via `APScheduler`.

2. **PokéAPI Engine (Mini-Projet 2)** :
   - Agrégation asynchrone des métriques de type via `asyncio` et `aiohttp` (Q2).
   - Comparateur de statistiques relatives (HP / Attaque).
   - Engine de simulation de duel au tour par tour sur 5 tours.
   - CLI interactive via `input()`.

3. **Dashboard Web Visual (Streamlit)** :
   - Application multi-pages avec carrousel TMDB et arène de combat animée PokéDex (`app.py`).

## 📁 Structure des Fichiers
- `01_core_api_engine.ipynb` : Notebook Jupyter complet.
- `app.py` : Code du Dashboard Streamlit.
- `requirements.txt` : Liste des dépendances Python.
