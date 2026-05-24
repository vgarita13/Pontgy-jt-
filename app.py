import streamlit as st
import pandas as pd
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------
# OLDAL BEÁLLÍTÁSOK
# ------------------------

st.set_page_config(
    page_title="Diák Pontverseny",
    page_icon="🏆",
    layout="wide"
)

st.markdown("""
<style>

/* =========================
   HÁTTÉR
========================= */

.stApp {
    background: linear-gradient(
        135deg,
        #f7f2ff 0%,
        #f1e9ff 45%,
        #faf7ff 100%
    );
    color: #2d1b69;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #6d56d6 0%,
        #7d64e8 45%,
        #8b72f2 100%
    );
    border-right: 2px solid rgba(255,255,255,0.15);
    box-shadow: 4px 0 25px rgba(120, 90, 255, 0.25);
}

/* sidebar összes szöveg */

/* sidebar szövegek */

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* =========================
   CÍMEK
========================= */

h1 {
    color: #24145c !important;
    font-weight: 800 !important;
    font-size: 48px !important;
}

h2, h3 {
    color: #35207a !important;
    font-weight: 700 !important;
}

/* pink underline */

h2::after {
    content: "";
    display: block;
    width: 90px;
    height: 4px;
    border-radius: 20px;
    margin-top: 8px;
    background: linear-gradient(
        90deg,
        #ff7adf,
        #c68cff
    );
}

/* =========================
   KÁRTYÁK
========================= */

div[data-testid="stVerticalBlock"] > div:has(.element-container) {
    border-radius: 24px;
}

/* =========================
   INPUTOK
========================= */

.stTextInput input,
.stNumberInput input {
    background: rgba(255,255,255,0.9) !important;
    border: 2px solid #e4d8ff !important;
    border-radius: 14px !important;
    color: #2d1b69 !important;
    padding: 0.5rem !important;
}

/* focus glow */

.stTextInput input:focus,
.stNumberInput input:focus {
    border: 2px solid #c68cff !important;
    box-shadow: 0 0 12px rgba(198,140,255,0.35) !important;
}

/* =========================
   GOMBOK
========================= */

.stButton > button {
    background: linear-gradient(
        135deg,
        #b07cff,
        #ea8cff
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 14px !important;

    font-weight: 700 !important;

    transition: 0.25s !important;

    box-shadow: 0 4px 15px rgba(176,124,255,0.25);
}

/* hover */

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 20px rgba(176,124,255,0.35);
}

/* =========================
   PLUSZ / MÍNUSZ GOMBOK
========================= */

button[kind="secondary"] {
    border-radius: 12px !important;

    border: 2px solid #e6d9ff !important;

    background: white !important;

    color: #9b5cff !important;

    font-weight: 700 !important;
}

button[kind="secondary"]:hover {
    background: #f7f0ff !important;
}

/* =========================
   ALERT BOX
========================= */

.stAlert {
    background: linear-gradient(
        90deg,
        #f4eaff,
        #f9f4ff
    ) !important;

    border-radius: 18px !important;

    border: 1px solid #e2d3ff !important;

    color: #7a4fd4 !important;
}

/* =========================
   TÁBLÁZAT
========================= */

[data-testid="stDataFrame"] {
    border-radius: 24px !important;

    overflow: hidden !important;

    border: 2px solid #e7dcff !important;

    background: rgba(255,255,255,0.8) !important;

    box-shadow: 0 4px 20px rgba(180,140,255,0.12);
}

/* =========================
   TÁBLÁZAT FEJLÉC
========================= */

thead tr th {
    background: #f3e9ff !important;

    color: #8a5ce6 !important;

    font-weight: 700 !important;
}

/* =========================
   SIDEBAR BLOKK
========================= */

/* sidebar input card */

[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stTextInput {

    background: rgba(255,255,255,0.08);

    padding: 14px;

    border-radius: 18px;

    margin-bottom: 12px;

    border: 1px solid rgba(255,255,255,0.08);
}

/* belső input */

[data-testid="stSidebar"] input {

    background: rgba(255,255,255,0.92) !important;

    border: none !important;

    box-shadow: none !important;

    border-radius: 14px !important;

    color: #3c2b7a !important;
}

/* =========================
   ELVÁLASZTÓ
========================= */

hr {
    border-color: rgba(255,255,255,0.2) !important;
}

/* =========================
   SCROLLBAR
========================= */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #c68cff;
    border-radius: 20px;
}

::-webkit-scrollbar-track {
    background: #f3ecff;
}
            
/* mini +/- gombok eltüntetése */

[data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# CÍM
# ------------------------

st.title("🏆 Pontverseny")
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
try:

    beallitas = supabase.table("maxpont").select("*").execute()

    if beallitas.data:
        alap_max_pont = beallitas.data[0]["max_pont"]
    else:
        alap_max_pont = 0

except:

    alap_max_pont = 0

max_pont = st.sidebar.number_input(
    "Maximum elérhető pont",
    min_value=0,
    value=alap_max_pont
)

supabase.table("maxpont").upsert({
    "id": 1,
    "max_pont": max_pont
}).execute()

st.sidebar.markdown("---")

# ------------------------
# PÁROSOK ADATAI
# ------------------------

FAJL = "pontok.json"

# ------------------------
# GITHUB BEÁLLÍTÁSOK
# ------------------------

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

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

if "pontok" not in st.session_state:

    try:

        adatbazis = supabase.table("pontok").select("*").execute()

        st.session_state.pontok = {}

        for sor in adatbazis.data:

            st.session_state.pontok[sor["paros"]] = sor["pont"]

    except:

        st.session_state.pontok = {}

# ------------------------
# MENTÉS
# ------------------------

def mentes():

    try:

        # régi adatok törlése
        supabase.table("pontok").delete().neq("id", 0).execute()

        # új adatok feltöltése
        for paros, pont in st.session_state.pontok.items():

            supabase.table("pontok").insert({
                "paros": paros,
                "pont": pont
            }).execute()

        st.toast("☁️ Supabase szinkron kész!")

    except Exception as e:

        st.error(f"Supabase hiba: {e}")
 
if admin:

    st.markdown("## 🎮 Pontozás")
    st.markdown("### ➕ Új páros hozzáadása")

    uj_paros = st.text_input("Páros neve")

    if st.button("Új páros hozzáadása"):

        if uj_paros != "":
            st.session_state.pontok[uj_paros] = 0
            mentes()

    for paros in list(st.session_state.pontok.keys()):

        col1, col2, col3, col4, col5, col6 = st.columns(
    [4, 2, 0.8, 0.8, 1.3, 0.8]
)

        with col1:
            st.write(paros)

        with col2:

            pont_valtozas = st.number_input(
                "Pont",
                min_value=1,
                max_value=100,
                value=1,
                key=f"input_{paros}",
                label_visibility="collapsed"
            )

        with col3:
            if st.button("➕", key=f"plus_{paros}"):
                uj_pont = st.session_state.pontok[paros] + pont_valtozas

                if uj_pont <= max_pont:

                    st.session_state.pontok[paros] = uj_pont

                    mentes()

                else:

                    st.warning("⚠️ Elérték a maximum pontot!")
                

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

df["Százalék"] = round(
    (df["Pont"] / max_pont) * 100,
    2
)

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

# ------------------------
# TÁBLÁZAT SZÍNEZÉS
# ------------------------

def szinezes(sor):

    jegy = sor["Jegy"]

    if jegy == 5:

        return [
            "background-color: #DDF4E4; color: #2E4A38"
        ] * len(sor)

    elif jegy == 4:

        return [
            "background-color: #E9E2FF; color: #43386B"
        ] * len(sor)

    elif jegy == 3:

        return [
            "background-color: #FFF3D6; color: #6B562A"
        ] * len(sor)

    elif jegy == 2:

        return [
            "background-color: #FFDCC8; color: #7A4426"
        ] * len(sor)

    else:

        return [
            "background-color: #FFD9E8; color: #7A3452"
        ] * len(sor)

# ------------------------
# STYLED DATAFRAME
# ------------------------

styled_df = (
    df.style
    .apply(szinezes, axis=1)
    .format({
        "Százalék": "{:.2f}%"
    })
)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=500
)
# ------------------------
# LEGJOBB PÁROS
# ------------------------

if df.empty:
    st.warning("Még nincs adat.")
    st.stop()
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