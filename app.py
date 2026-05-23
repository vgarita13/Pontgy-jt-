import streamlit as st
import pandas as pd
import json
import os
import time
from github import Github
import base64
import requests

# ------------------------
# OLDAL BEÁLLÍTÁSOK
# ------------------------

st.set_page_config(
    page_title="Diák Pontverseny",
    page_icon="🏆",
    layout="wide"
)

# ------------------------
# CÍM
# ------------------------

st.title("🏆 Diák Pontverseny")
st.markdown("## Aktuális állás")

# ------------------------
# TANÁRI MÓD
# ------------------------

jelszo = st.sidebar.text_input(
    "Tanári jelszó",
    type="password"
)

admin = jelszo == "titok123"

# ------------------------
# MAXIMUM PONT
# ------------------------

max_pont = st.sidebar.number_input(
    "Maximum elérhető pont",
    min_value=1,
    value=20
)

st.sidebar.markdown("---")

# ------------------------
# PÁROSOK ADATAI
# ------------------------

FAJL = "pontok.json"

# ------------------------
# GITHUB BEÁLLÍTÁSOK
# ------------------------

GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

REPO_NEV = "vgarita13/Pontgy-jt-"

JSON_FAJL = "pontok.json"

# ------------------------
# BETÖLTÉS
# ------------------------

# ------------------------
# GITHUB RAW JSON URL
# ------------------------

# ------------------------
# ELSŐ BETÖLTÉS
# ------------------------

if "pontok" not in st.session_state or not admin:
    try:

        RAW_JSON_URL = f"https://raw.githubusercontent.com/vgarita13/Pontgy-jt-/main/pontok.json?t={time.time()}"

        response = requests.get(RAW_JSON_URL)

        if response.status_code == 200:

            st.session_state.pontok = response.json()

        else:

            st.session_state.pontok = {
                "Anna – Bence": 13,
                "Luca – Marci": 17,
                "Petra – Dávid": 8,
                "Nóri – Ádám": 19,
                "Zsófi – Balázs": 11
            }

    except:

        st.session_state.pontok = {
            "Anna – Bence": 13,
            "Luca – Marci": 17,
            "Petra – Dávid": 8,
            "Nóri – Ádám": 19,
            "Zsófi – Balázs": 11
        }

# ------------------------
# MENTÉS
# ------------------------

def mentes():

    # ------------------------
    # LOKÁLIS JSON MENTÉS
    # ------------------------

    with open(FAJL, "w", encoding="utf-8") as f:

        json.dump(
            st.session_state.pontok,
            f,
            ensure_ascii=False,
            indent=4
        )

    # ------------------------
    # GITHUB SZINKRON
    # ------------------------

    try:

        g = Github(GITHUB_TOKEN)

        repo = g.get_repo(REPO_NEV)

        with open(FAJL, "r", encoding="utf-8") as f:

            tartalom = f.read()

        file = repo.get_contents(JSON_FAJL)

        repo.update_file(
            JSON_FAJL,
            "Automatikus pontfrissítés",
            tartalom,
            file.sha
        )

        st.toast("☁️ GitHub szinkron kész!")

    except Exception as e:

        st.error(f"GitHub hiba: {e}")

if admin:

    st.markdown("## 🎮 Pontozás")
    st.markdown("### ➕ Új páros hozzáadása")

    uj_paros = st.text_input("Páros neve")

    if st.button("Új páros hozzáadása"):

        if uj_paros != "":
            st.session_state.pontok[uj_paros] = 0
            mentes()

    for paros in list(st.session_state.pontok.keys()):

        col1, col2, col3, col4, col5, col6 = st.columns([4,2,1,1,2,1])

        with col1:
            st.write(paros)

        with col2:

            pont_valtozas = st.number_input(
                "Pont",
                min_value=1,
                max_value=100,
                value=1,
                key=f"input_{paros}"
            )

        with col3:
            if st.button("➕", key=f"plus_{paros}"):
                st.session_state.pontok[paros] += pont_valtozas
                mentes()

        with col4:
            if st.button("➖", key=f"minus_{paros}"):
                st.session_state.pontok[paros] -= pont_valtozas
                mentes()

        with col5:
            st.write(f"⭐ {st.session_state.pontok[paros]} pont")

        with col6:
            if st.button("❌", key=f"delete_{paros}"):

                del st.session_state.pontok[paros]
                mentes()

                st.rerun()

df = pd.DataFrame({
    "Páros": list(st.session_state.pontok.keys()),
    "Pont": list(st.session_state.pontok.values())
})

# DataFrame


# ------------------------
# SZÁZALÉK SZÁMÍTÁS
# ------------------------

df["Százalék"] = round((df["Pont"] / max_pont) * 100, 1)

# ------------------------
# JEGY SZÁMÍTÁS
# ------------------------

def jegy(szazalek):
    if szazalek >= 80:
        return 5
    elif szazalek >= 60:
        return 4
    elif szazalek >= 40:
        return 3
    elif szazalek >= 25:
        return 2
    else:
        return 1


df["Jegy"] = df["Százalék"].apply(jegy)

# ------------------------
# RANGSOR
# ------------------------

df = df.sort_values(by="Pont", ascending=False)
df = df.reset_index(drop=True)

# ------------------------
# HELYEZÉS
# ------------------------

helyezesek = []

for i in range(len(df)):
    if i == 0:
        helyezesek.append("🥇")
    elif i == 1:
        helyezesek.append("🥈")
    elif i == 2:
        helyezesek.append("🥉")
    else:
        helyezesek.append(f"#{i+1}")


df.insert(0, "Hely", helyezesek)

# ------------------------
# SZÍNEZÉS
# ------------------------

def szinezes(sor):
    if sor["Jegy"] == 5:
        return ['background-color: #1f7a1f'] * len(sor)
    elif sor["Jegy"] == 4:
        return ['background-color: #2e8b57'] * len(sor)
    elif sor["Jegy"] == 3:
        return ['background-color: #b8860b'] * len(sor)
    elif sor["Jegy"] == 2:
        return ['background-color: #cc7000'] * len(sor)
    else:
        return ['background-color: #8b0000'] * len(sor)

# ------------------------
# INFO DOBOZ
# ------------------------

st.info(f"📌 Eddig maximum {max_pont} pontot lehetett elérni.")

# ------------------------
# TÁBLÁZAT
# ------------------------

st.dataframe(
    df.style.apply(szinezes, axis=1),
    use_container_width=True,
    height=500
)

# ------------------------
# LEGJOBB PÁROS
# ------------------------

elso = df.iloc[0]

st.success(
    f"🏆 Jelenlegi első helyezett: {elso['Páros']} ({elso['Pont']} pont)"
)

# ------------------------
# OLDALSÁV INFORMÁCIÓ
# ------------------------

st.sidebar.markdown("## Jegyhatárok")
st.sidebar.markdown("- 80% → 5")
st.sidebar.markdown("- 60% → 4")
st.sidebar.markdown("- 40% → 3")
st.sidebar.markdown("- 25% → 2")
st.sidebar.markdown("- 0% → 1")

# ------------------------
# FRISSÍTÉSI ÚTMUTATÓ
# ------------------------

st.markdown("---")
st.markdown("### ✏️ Pontok frissítése")
st.markdown(
    "A pontokat a tanári módban tudod szerkeszteni."
)

st.markdown("### 🚀 Indítás")
st.code("python -m streamlit run app.py")