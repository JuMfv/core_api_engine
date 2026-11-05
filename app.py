import os
import time
import math
import random
import asyncio
import aiohttp
import requests
import streamlit as st

# ---------------------------------------------------------
# Configuration globale de la page
# ---------------------------------------------------------
st.set_page_config(
    page_title="API Core Engine — Visual Hub",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style CSS minimaliste et épuré
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stApp { background-color: #0f172a; }
    .css-1d3av2a { background-color: #1e293b; }
    div[data-testid="stMetricValue"] { color: #38bdf8; font-weight: 700; }
    .stButton>button {
        background-color: #3b82f6; color: white; border-radius: 8px;
        border: none; padding: 10px 24px; font-weight: 600; transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #2563eb; transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Variables & API Keys
# ---------------------------------------------------------
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "777ab01b524ea3312667e340da77de82")
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# ---------------------------------------------------------
# Navigation - Page de Garde
# ---------------------------------------------------------
if 'view' not in st.session_state:
    st.session_state.view = 'home'

if st.session_state.view == 'home':
    st.markdown("<h1 style='text-align: center; margin-top: 50px; font-size: 3rem;'>API Core Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; margin-bottom: 50px;'>Sélectionnez un univers pour explorer le moteur visuel</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: #1e293b; border-radius: 16px; padding: 40px; text-align: center; border: 1px solid #334155;">
            <h2 style="color: #38bdf8;">🎬 TMDB Cinema Hub</h2>
            <p style="color: #94a3b8;">Catalogue défilant, posters HD, métriques de popularité et catégories de films.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Lancer TMDB Cinema", use_container_width=True):
            st.session_state.view = 'tmdb'
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background: #1e293b; border-radius: 16px; padding: 40px; text-align: center; border: 1px solid #334155;">
            <h2 style="color: #ef4444;">⚡ PokéDex Arena</h2>
            <p style="color: #94a3b8;">Fiches visuelles, arène de combat animée et statistiques dynamiques.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Lancer PokéDex Arena", use_container_width=True):
            st.session_state.view = 'pokedex'
            st.rerun()

# ---------------------------------------------------------
# VUE 1 : TMDB CINEMA HUB (Vrais Appels API & Carrousel)
# ---------------------------------------------------------
elif st.session_state.view == 'tmdb':
    st.button("← Retour au Menu", on_click=lambda: st.session_state.update(view='home'))
    st.title("🎬 TMDB Cinema Catalog")

    # Sélection de la Catégorie / Genre
    category = st.radio(
        "Catégorie de films :",
        ["Popular", "Top Rated", "Now Playing", "Upcoming"],
        horizontal=True
    )

    category_endpoint = {
        "Popular": "movie/popular",
        "Top Rated": "movie/top_rated",
        "Now Playing": "movie/now_playing",
        "Upcoming": "movie/upcoming"
    }[category]

    # Appel API Réel
    url = f"https://api.themoviedb.org/3/{category_endpoint}?api_key={TMDB_API_KEY}&language=fr-FR&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json().get("results", [])[:10]

        st.markdown("### 🍿 Catalogue en Défilement (Top 10)")
        
        # Grille visuelle de cartes / posters
        cols = st.columns(5)
        for idx, movie in enumerate(movies[:5]):
            with cols[idx]:
                poster_path = movie.get("poster_path")
                img_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else "https://via.placeholder.com/500x750"
                st.image(img_url, use_column_width=True)
                st.subheader(movie.get("title"))
                st.caption(f"⭐ {movie.get('vote_average')}/10 | 📅 {movie.get('release_date')[:4] if movie.get('release_date') else 'N/A'}")

        cols2 = st.columns(5)
        for idx, movie in enumerate(movies[5:10]):
            with cols2[idx]:
                poster_path = movie.get("poster_path")
                img_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else "https://via.placeholder.com/500x750"
                st.image(img_url, use_column_width=True)
                st.subheader(movie.get("title"))
                st.caption(f"⭐ {movie.get('vote_average')}/10 | 📅 {movie.get('release_date')[:4] if movie.get('release_date') else 'N/A'}")
    else:
        st.error("Erreur de connexion à l'API TMDB. Vérifiez votre clé d'accès.")

# ---------------------------------------------------------
# VUE 2 : POKÉDEX ARENA (Vrais Appels API & Animations)
# ---------------------------------------------------------
elif st.session_state.view == 'pokedex':
    st.button("← Retour au Menu", on_click=lambda: st.session_state.update(view='home'))
    st.title("⚡ PokéDex Visual Engine")

    tab1, tab2 = st.tabs(["🎮 Arène de Combat Animée", "🔍 Fiche & Statistiques"])

    # TAB 1 : Combat Animé avec Vrais Sprites
    with tab1:
        st.subheader("Simulateur de Duel 5 Tours")
        c1, c2 = st.columns(2)
        with c1:
            p1_input = st.text_input("Pokémon 1 :", value="charizard").lower()
        with c2:
            p2_input = st.text_input("Pokémon 2 :", value="blastoise").lower()

        if st.button("🔥 Lancer le Combat !", use_container_width=True):
            r1 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{p1_input}")
            r2 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{p2_input}")

            if r1.status_code == 200 and r2.status_code == 200:
                d1, d2 = r1.json(), r2.json()

                # Sprites officiels
                sprite1 = d1["sprites"]["other"]["official-artwork"]["front_default"] or d1["sprites"]["front_default"]
                sprite2 = d2["sprites"]["other"]["official-artwork"]["front_default"] or d2["sprites"]["front_default"]

                # Extractions des stats
                stats1 = {s["stat"]["name"]: s["base_stat"] for s in d1["stats"]}
                stats2 = {s["stat"]["name"]: s["base_stat"] for s in d2["stats"]}

                hp1_max, hp1_curr = stats1.get("hp", 100), stats1.get("hp", 100)
                hp2_max, hp2_curr = stats2.get("hp", 100), stats2.get("hp", 100)

                # Affichage des combattants
                col_a, col_vs, col_b = st.columns([2, 1, 2])
                with col_a:
                    st.image(sprite1, width=200)
                    st.markdown(f"### {d1['name'].capitalize()}")
                    hp_bar1 = st.progress(1.0)
                with col_vs:
                    st.markdown("<h1 style='text-align: center; margin-top: 80px; color: #ef4444;'>VS</h1>", unsafe_allow_html=True)
                with col_b:
                    st.image(sprite2, width=200)
                    st.markdown(f"### {d2['name'].capitalize()}")
                    hp_bar2 = st.progress(1.0)

                # Animation du Combat tour par tour
                st.markdown("---")
                battle_log = st.empty()

                for turn in range(1, 6):
                    time.sleep(1.2)  # Effet visuel d'attente
                    dmg1 = math.ceil((stats1.get("attack", 50) / max(1, stats2.get("defense", 50))) * 10 * random.uniform(0.85, 1.0))
                    dmg2 = math.ceil((stats2.get("attack", 50) / max(1, stats1.get("defense", 50))) * 10 * random.uniform(0.85, 1.0))

                    hp2_curr = max(0, hp2_curr - dmg1)
                    hp1_curr = max(0, hp1_curr - dmg2)

                    hp_bar1.progress(hp1_curr / hp1_max)
                    hp_bar2.progress(hp2_curr / hp2_max)

                    battle_log.markdown(f"""
                    <div style="background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #ef4444;">
                        <h4>Tour {turn} / 5</h4>
                        <p>💥 <b>{d1['name'].capitalize()}</b> inflige <b>{dmg1}</b> dégâts !</p>
                        <p>💥 <b>{d2['name'].capitalize()}</b> inflige <b>{dmg2}</b> dégâts !</p>
                    </div>
                    """, unsafe_allow_html=True)

                winner = d1['name'].capitalize() if hp1_curr > hp2_curr else (d2['name'].capitalize() if hp2_curr > hp1_curr else "Égalité")
                st.balloons()
                st.success(f"🏆 Vainqueur du combat : {winner} !")
            else:
                st.error("Impossible de récupérer les données de l'un des Pokémon.")

    # TAB 2 : Fiches Visuelles
    with tab2:
        search_target = st.text_input("Rechercher un Pokémon :", value="pikachu").lower()
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{search_target}")

        if res.status_code == 200:
            data = res.json()
            col_img, col_info = st.columns([1, 2])

            with col_img:
                st.image(data["sprites"]["other"]["official-artwork"]["front_default"], width=280)
            with col_info:
                st.markdown(f"## {data['name'].capitalize()} (#{data['id']})")
                types = [t["type"]["name"].upper() for t in data["types"]]
                st.write(" **Types** : " + " | ".join(types))

                for stat in data["stats"]:
                    s_name = stat["stat"]["name"].upper()
                    s_val = stat["base_stat"]
                    st.text(f"{s_name}: {s_val}")
                    st.progress(min(1.0, s_val / 150))
