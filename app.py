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

/* ===== HÁTTÉR ===== */

.stApp {
    background: linear-gradient(
        135deg,
        #f6f1ff 0%,
        #efe7ff 45%,
        #f9f4ff 100%
    );
    color: #2d1b69;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #8f6bff 0%,
        #7b5cff 100%
    );
    border-right: 3px solid #cdb8ff;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== CÍMEK ===== */

h1, h2, h3 {
    color: #2d1b69 !important;
    font-weight: 700;
}

/* ===== GOMBOK ===== */

.stButton > button {
    background: linear-gradient(
        135deg,
        #b388ff,
        #e6b3ff
    );
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.4rem 1rem;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(
        135deg,
        #9f70ff,
        #d98cff
    );
}

/* ===== INPUTOK ===== */

.stTextInput input,
.stNumberInput input {
    border-radius: 12px !important;
    border: 2px solid #dccbff !important;
    background-color: white !important;
    color: #2d1b69 !important;
}

/* ===== TÁBLÁZAT ===== */

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 2px solid #e5d8ff;
}

/* ===== INFO BOX ===== */

.stAlert {
    border-radius: 14px;
    background-color: #efe5ff !important;
    color: #6b42c7 !important;
}

/* ===== ELVÁLASZTÓ ===== */

hr {
    border-color: #ccb8ff;
}

/* ===== SIDEBAR BLOKK ===== */

[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stTextInput {
    background: rgba(255,255,255,0.12);
    padding: 10px;
    border-radius: 16px;
}

/* ===== PLUSZ-MÍNUSZ GOMB ===== */

button[kind="secondary"] {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

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