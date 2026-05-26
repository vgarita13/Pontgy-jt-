import streamlit as st
import pandas as pd
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="Diák Pontverseny",
    page_icon="🏆",
    layout="wide"
)

# ------------------------
# CSOPORTOK BETÖLTÉSE
# ------------------------

try:

    csoport_adatok = (
        supabase
        .table("csoportok")
        .select("*")
        .execute()
    )


    csoportok = [
        c["nev"]
        for c in csoport_adatok.data
    ]

except:

    csoportok = []


# ------------------------
# CSOPORT VÁLASZTÁS
# ------------------------

if "aktiv_csoport" not in st.session_state:
    st.session_state.aktiv_csoport = None

if st.session_state.aktiv_csoport is None:

    st.markdown("""
    <style>

    .chooser-title{
        text-align:center;
        font-size:72px;
        font-weight:800;
        color:#2d1b7d;
        margin-top:40px;
        margin-bottom:10px;
    }

    .chooser-sub{
        text-align:center;
        font-size:28px;
        color:#8b72c9;
        margin-bottom:60px;
    }

    div[data-testid="column"] .stButton > button

        width:100%;
        height:220px;

        border:none !important;
        border-radius:34px !important;

        background:rgba(255,255,255,0.72) !important;
        backdrop-filter: blur(12px);

        color:#2d1b7d !important;

        font-size:42px !important;
        font-weight:800 !important;

        box-shadow:
            0 10px 35px rgba(170,120,255,0.15);

        transition:0.25s;
    }

    div[data-testid="column"] .stButton > button

        transform:
            translateY(-6px)
            scale(1.02);

        background:white !important;

        color:#7c3aed !important;

        box-shadow:
            0 18px 40px rgba(170,120,255,0.28);
    }

    .stApp{
        background:
            radial-gradient(circle at top left,
            rgba(190,150,255,0.28),
            transparent 25%),

            radial-gradient(circle at bottom right,
            rgba(210,170,255,0.28),
            transparent 25%),

            linear-gradient(
                135deg,
                #f8f3ff,
                #f1e8ff
            );
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chooser-title">
        🏆 Válassz csoportot
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chooser-sub">
        ✨ Kattints a csoportodra a folytatáshoz!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

if "admin" not in st.session_state:
    st.session_state["admin"] = False


if st.session_state.aktiv_csoport is None:

    st.markdown("### 👩‍🏫 Tanári mód")

    jelszo = st.text_input(
        "Tanári jelszó",
        type="password"
    )

    if jelszo == "titok123":
        st.session_state["admin"] = True

    cols = st.columns(3)

    for i, csoport in enumerate(csoportok):

        with cols[i % 3]:

            if st.button(csoport, key=f"group_{csoport}"):

                st.session_state.aktiv_csoport = csoport
                st.rerun()

    st.stop()


aktiv_csoport = st.session_state.aktiv_csoport

admin = st.session_state["admin"]

# ------------------------
# OLDAL BEÁLLÍTÁSOK
# ------------------------


st.markdown("""
<style>

/* =========================
   HÁTTÉR
========================= */

.stApp {
    background:
        radial-gradient(
            circle at top left,
            #ffffff 0%,
            #f7f0ff 30%,
            #efe5ff 70%,
            #f8f5ff 100%
    );
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #5d49d8 0%,
        #6f58eb 45%,
        #8269f3 100%
    );

    border-right: none;

    box-shadow: 4px 0 30px rgba(95, 70, 255, 0.25);
}

/* sidebar belső padding */

section[data-testid="stSidebar"] .block-container {

    padding-top: 0rem;

    padding-left: 1rem;

    padding-right: 1rem;
}

/* sidebar szövegek */

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span {

    color: white !important;
}

/* input doboz */

[data-testid="stSidebar"] input {

    background: rgba(255,255,255,0.96) !important;

    border: none !important;

    border-radius: 18px !important;

    color: #3d2a75 !important;

    box-shadow: none !important;

    padding: 12px !important;

    font-size: 18px !important;
}

/* szem ikon */

[data-testid="stSidebar"] svg {

    color: #4b3b91 !important;
}

/* jegyhatárok */

.grade-list li{

    display:flex;

    align-items:center;

    margin-bottom:18px;
}
.grade-percent{

    width:32px;

    margin-left:10px;

    font-variant-numeric: tabular-nums;
}

.grade-arrow{

    width:16px;

    text-align:center;
}

.grade-number{

    width:18px;

    text-align:left;
}
            
/* színes pöttyök */

.dot {

    width:16px;

    height:16px;

    min-width:16px;

    min-height:16px;

    border-radius:50%;

    display:inline-block;

    flex-shrink:0;
}

.green { background: #c7f0d8; }

.purple { background: #d9d0ff; }

.yellow { background: #ffe7a3; }

.orange { background: #ffd1a8; }

.red { background: #ffb7cc; }

/* rózsaszín vonal */

.pink-line {

    width: 80px;

    height: 5px;

    border-radius: 999px;

    background: #ff9de1;

    margin-bottom: 24px;
}

/* =========================
   CÍMEK
========================= */

h1 {

    color: #24145c !important;

    font-weight: 800 !important;

    font-size: 48px !important;

    margin-top:0px !important;
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

/* =========================
   FŐ GOMBOK
========================= */

div[data-testid="stVerticalBlock"] .stButton > button {

    background: linear-gradient(
        135deg,
        #a855f7,
        #c084fc
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 16px !important;

    font-weight: 700 !important;

    transition: 0.25s !important;

    box-shadow:
        0 8px 24px rgba(168,85,247,0.25);

    height: 48px;
}

/* hover */

div[data-testid="stVerticalBlock"] .stButton > button:hover {

    background: linear-gradient(
        135deg,
        #9333ea,
        #b066ff
    ) !important;

    color: white !important;

    transform: translateY(-2px);

    box-shadow:
        0 10px 28px rgba(168,85,247,0.35);
}

/* =========================
   SIDEBAR GOMB
========================= */

section[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    background:
        rgba(255,255,255,0.14) !important;

    border:
        1px solid rgba(255,255,255,0.18) !important;

    backdrop-filter: blur(12px);

    color: white !important;

    border-radius: 18px !important;

    font-weight: 700 !important;

    height: 52px;

    transition: 0.25s;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.10);
}

/* sidebar hover */

section[data-testid="stSidebar"] .stButton > button:hover {

    background:
        rgba(255,255,255,0.22) !important;

    color: white !important;

    transform: translateY(-2px);

    border:
        1px solid rgba(255,255,255,0.28) !important;
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

    border-radius: 28px !important;

    overflow: hidden !important;

    border: 2px solid rgba(255,170,255,0.35) !important;

    background:
        rgba(255,255,255,0.58) !important;

    backdrop-filter: blur(18px);

    box-shadow:
        0 10px 35px rgba(180,120,255,0.18),
        0 0 0 1px rgba(255,255,255,0.25);
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


/* belső input */

[data-testid="stSidebar"] input {

    background: rgba(255,255,255,0.92) !important;

    border: none !important;

    box-shadow: none !important;

    border-radius: 14px !important;

    color: #3c2b7a !important;
}
            
/* sidebar szövegek */

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span {
    color: white !important;
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

# =========================
# HERO / FELSŐ RÉSZ
# =========================



# =========================
# HERO CSS
# =========================

st.markdown("""
<style>
            
/* =========================
   LOGO WRAP
========================= */

.logo-wrap{

    display:flex;

    flex-direction:column;

    align-items:center;

    justify-content:center;

    margin-top: -60px;

    margin-bottom:10px;
    padding-top:0px;
}


/* =========================
   LOGO CÍM
========================= */

.logo-title{

    text-align:center;

    width:100%;

    font-size:30px;

    font-weight:900;

    line-height:1.05;

    color:white;

    letter-spacing:-0.5px;

    margin-top:-30px;

    margin-bottom:25px;

    text-shadow:
        0 4px 18px rgba(0,0,0,0.22);
}
            
/* LOGO KÉP */

[data-testid="stSidebar"] img {

    pointer-events: none !important;

    user-select: none !important;

    -webkit-user-drag: none !important;
}
            
/* =========================
   STREAMLIT TOOLBAR ELREJTÉS
========================= */

[data-testid="stElementToolbar"]{
    display:none !important;
}

[data-testid="stElementToolbarButton"]{
    display:none !important;
}

/* =========================
   RÓZSASZÍN VONAL
========================= */
            

</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.sidebar.markdown('<div class="logo-wrap">', unsafe_allow_html=True)

st.sidebar.image(
    "trophy.png",
    width=230
)

st.sidebar.markdown("""
<div class="logo-title">
    Diák<br>Pontverseny
</div>
</div>
""", unsafe_allow_html=True)



st.sidebar.markdown(f"""
<div style="
    margin-top:12px;
    margin-bottom:10px;
    background:rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.18);
    border-radius:18px;
    padding:12px 16px;
    text-align:center;
    backdrop-filter:blur(10px);
">

<div style="
    color:rgba(255,255,255,0.75);
    font-size:14px;
    font-weight:600;
    margin-bottom:6px;
">
📚 Aktív csoport
</div>

<div style="
    color:white;
    font-size:26px;
    font-weight:800;
">
{aktiv_csoport}
</div>

</div>
""", unsafe_allow_html=True)


# ------------------------
# CÍM
# ------------------------


st.markdown("## Aktuális állás")

# ------------------------
# TANÁRI MÓD
# ------------------------

# ------------------------
# MAXIMUM PONT
# ------------------------

try:

    beallitas = (
        supabase
        .table("maxpont")
        .select("*")
        .eq("csoport", aktiv_csoport)
        .execute()
    )

    if beallitas.data:

        alap_max_pont = beallitas.data[0]["max_pont"]

    else:

        alap_max_pont = 100

        supabase.table("maxpont").insert({
            "csoport": aktiv_csoport,
            "max_pont": 100
        }).execute()

except:

    alap_max_pont = 100


if admin:

    max_pont = st.sidebar.number_input(
        "Maximum elérhető pont",
        min_value=1,
        value=alap_max_pont
    )

    supabase.table("maxpont").upsert({
        "csoport": aktiv_csoport,
        "max_pont": max_pont
    }).execute()

else:

    max_pont = alap_max_pont

    st.sidebar.markdown(f"""
    <div style="
        margin-top:10px;
        background:rgba(255,255,255,0.14);
        border:1px solid rgba(255,255,255,0.18);
        border-radius:18px;
        padding:14px 16px;
        color:white;
        font-size:18px;
        font-weight:700;
        text-align:center;
        backdrop-filter:blur(10px);
    ">
        🎯 Aktuális max pont<br>
        <span style="
            font-size:32px;
            font-weight:900;
        ">
            {max_pont}
        </span>
    </div>
    """, unsafe_allow_html=True)

# ------------------------
# ELSŐ BETÖLTÉS
# ------------------------

if (
    "pontok" not in st.session_state
    or st.session_state.get("betoltott_csoport") != aktiv_csoport
):

    try:

        adatbazis = (
            supabase
            .table("pontok")
            .select("*")
            .eq("csoport", aktiv_csoport)
            .execute()
        )

        st.session_state.pontok = {}
        st.session_state.betoltott_csoport = aktiv_csoport

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
        supabase.table("pontok") \
            .delete() \
            .eq("csoport", aktiv_csoport) \
            .execute()

        # új adatok feltöltése
        for paros, pont in st.session_state.pontok.items():

            supabase.table("pontok").insert({
                "csoport": aktiv_csoport,
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
# SOR SZÍNEZÉS
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
# TÁBLÁZAT
# ------------------------


# ------------------------
# RENDEZÉS
# ------------------------

df = df.sort_values(
    by="Pont",
    ascending=False
)

df = df.reset_index(drop=True)

# ------------------------
# HELYEZÉSEK
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
# ELSŐ HELYEZETT
# ------------------------


# ------------------------
# LEGJOBB PÁROS
# ------------------------


# ------------------------
# LEGJOBB PÁROS
# ------------------------

if df.empty:

    st.info("Ebben a csoportban még nincs pont.")

else:

    elso = df.iloc[0]

    st.markdown(f"""
    <div style="
        background: linear-gradient(
            90deg,
            #eefdf2,
            #f8fff9
        );
        border:1px solid #d9f5df;
        border-radius:24px;
        padding:22px 26px;
        color:#237346;
        font-size:28px;
        font-weight:700;
        box-shadow:
            0 6px 20px rgba(125,219,154,0.10);
        overflow:hidden;
    ">

    🏆 Jelenlegi első helyezett:
    {elso['Páros']}
    ({elso['Pont']} pont)

    </div>
    """, unsafe_allow_html=True)

# ------------------------
# OLDALSÁV INFORMÁCIÓ
# ------------------------

st.sidebar.markdown("""
## Jegyhatárok


<ul class="grade-list">

<li>
    <span class="dot green"></span>
    <span class="grade-percent">80%</span>
    <span class="grade-arrow">→</span>
    <span class="grade-number">5</span>
</li>

<li>
    <span class="dot purple"></span>
    <span class="grade-percent">60%</span>
    <span class="grade-arrow">→</span>
    <span class="grade-number">4</span>
</li>

<li>
    <span class="dot yellow"></span>
    <span class="grade-percent">40%</span>
    <span class="grade-arrow">→</span>
    <span class="grade-number">3</span>
</li>

<li>
    <span class="dot orange"></span>
    <span class="grade-percent">25%</span>
    <span class="grade-arrow">→</span>
    <span class="grade-number">2</span>
</li>

<li>
    <span class="dot red"></span>
    <span class="grade-percent">0%</span>
    <span class="grade-arrow">→</span>
    <span class="grade-number">1</span>
</li>

</ul>
""", unsafe_allow_html=True)

if st.sidebar.button("⬅️ Csoportváltás"):

    st.session_state.aktiv_csoport = None
    st.rerun()

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