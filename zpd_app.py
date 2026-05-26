# =============================================================
# ZPD VĒRTĒŠANAS ONLINE RĪKS
# Streamlit web aplikācija skolotājiem un ZPD atbildīgajam
# =============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
import json
from datetime import datetime

# --- Iestatījumi ---
MAPE = r"C:\Users\ilona\OneDrive\Dators\Phyton"
DATU_FAILS = os.path.join(MAPE, "zpd_rezultati.csv")

# Kritēriji un to maksimālie punkti
KRITERIJI = {
    "Koncepcija": 16,
    "Literatūra": 10,
    "Metodes": 10,
    "Rezultāti": 20,
    "Secinājumi": 6,
    "Ētika": 2,
    "Noformējums": 12,
    "Pienesums": 4,
    "Aizstāvēšana": 10,
    "MI izmantošana": 10
}

# =============================================================
# LAPAS KONFIGURĀCIJA
# =============================================================
st.set_page_config(
    page_title="ZPD Vērtēšanas rīks",
    page_icon="🎓",
    layout="wide"
)

# =============================================================
# SĀNU IZVĒLNE
# =============================================================
st.sidebar.title("🎓 ZPD Vērtēšanas rīks")
st.sidebar.markdown("---")

lapa = st.sidebar.radio(
    "Izvēlies sadaļu:",
    ["📝 Ievadīt vērtējumu", "📊 Skatīt datus", "📈 Statistika un TOP 10"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Lietošanas pamācība:**\n\n"
                "1. Skolotājs: *Ievadīt vērtējumu*\n"
                "2. ZPD atbildīgais: *Statistika*")

# =============================================================
# FUNKCIJA — ielādēt datus
# =============================================================
def ieladet_datus():
    if os.path.exists(DATU_FAILS):
        return pd.read_csv(DATU_FAILS)
    else:
        return pd.DataFrame()

# =============================================================
# AI ANALĪZES FUNKCIJA
# =============================================================
def ai_analize(df):
    # Sagatavojam statistiku AI iesūtīšanai
    vid_balle = df["Balle"].mean()
    maks_punkti = df["Kopā"].max()
    min_punkti = df["Kopā"].min()
    skolenu_skaits = len(df)
    top10_skaits = len(df[(df["Mācību gads"] == "2025/2026") & (df["Balle"] >= 8)])

    # Vidējie punkti pa kritērijiem
    kriteriju_videjie = {}
    for k, maks in KRITERIJI.items():
        if k in df.columns:
            videjais = df[k].mean()
            kriteriju_videjie[k] = f"{videjais:.1f}/{maks}"

    kriteriji_teksts = "\n".join([f"  - {k}: {v}" for k, v in kriteriju_videjie.items()])

    prompt = f"""Tu esi pieredzējis izglītības eksperts Latvijā. 
Analizē šos ZPD (zinātniski pētnieciskais darbs) vērtēšanas rezultātus un sniedz īsu, konstruktīvu analīzi latviešu valodā.

STATISTIKA:
- Skolēnu skaits: {skolenu_skaits}
- Vidējā balle: {vid_balle:.2f}/10
- Augstākie punkti: {maks_punkti:.0f}/100
- Zemākie punkti: {min_punkti:.0f}/100
- Skolēni uz novadu (balle ≥8, 2025/2026): {top10_skaits}

Vidējie punkti pa kritērijiem:
{kriteriji_teksts}

Sniedz:
1. Īsu kopsavilkumu (2-3 teikumi)
2. Stiprākos kritērijus (kuros skolēni gūst visvairāk punktu)
3. Vājākos kritērijus (kur ir uzlabojumu iespējas)
4. Vienu konkrētu ieteikumu skolotājiem

Atbildi latviešu valodā, draudzīgā un profesionālā tonī. Maksimums 200 vārdi."""

    API_URL = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        atbilde = requests.post(API_URL, headers=headers, json=body, timeout=30)
        dati = atbilde.json()
        return dati["content"][0]["text"]
    except Exception as e:
        return f"❌ Kļūda sazinoties ar AI: {e}"

# =============================================================
# LAPA 1: IEVADĪT VĒRTĒJUMU
# =============================================================
if lapa == "📝 Ievadīt vērtējumu":
    st.title("📝 Ievadīt skolēna ZPD vērtējumu")
    st.markdown("Aizpildi skolēna datus un atzīmē punktus katrā kritērijā.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        vards = st.text_input("Vārds *")
        klase = st.selectbox("Klase *", 
                             ["10A", "10B", "10C", "10D", "10E", "10F",
                              "11A", "11B", "11C", "12A", "12B"])
    with col2:
        uzvards = st.text_input("Uzvārds *")
        gads = st.selectbox("Mācību gads *", 
                           ["2023/2024", "2024/2025", "2025/2026"],
                           index=2)

    st.markdown("---")
    st.subheader("🎯 Vērtēšanas kritēriji")
    
    punkti = {}
    col1, col2 = st.columns(2)
    kritēriji_saraksts = list(KRITERIJI.items())
    puse = len(kritēriji_saraksts) // 2
    
    with col1:
        for kritērijs, maks in kritēriji_saraksts[:puse + 1]:
            punkti[kritērijs] = st.number_input(
                f"{kritērijs} (0-{maks})",
                min_value=0, max_value=maks, value=0, step=1,
                key=f"k_{kritērijs}"
            )
    with col2:
        for kritērijs, maks in kritēriji_saraksts[puse + 1:]:
            punkti[kritērijs] = st.number_input(
                f"{kritērijs} (0-{maks})",
                min_value=0, max_value=maks, value=0, step=1,
                key=f"k_{kritērijs}"
            )

    st.markdown("---")
    kopa = sum(punkti.values())
    balle = round(kopa / 10) if kopa > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Kopā punkti", f"{kopa}/100")
    with col2:
        st.metric("Balle", balle)
    with col3:
        if balle >= 8:
            st.success("✅ Uz novadu!")
        elif balle >= 5:
            st.info("📗 Ieskaitīts")
        else:
            st.warning("⚠️ Neieskaitīts")

    st.markdown("---")
    if st.button("💾 Saglabāt vērtējumu", type="primary", use_container_width=True):
        if not vards or not uzvards:
            st.error("❌ Lūdzu aizpildi vārdu un uzvārdu!")
        else:
            jauns_ieraksts = {
                "Vārds": vards, "Uzvārds": uzvards,
                "Klase": klase, "Mācību gads": gads,
                **punkti, "Kopā": float(kopa), "Balle": balle
            }
            df = ieladet_datus()
            df_jauns = pd.concat([df, pd.DataFrame([jauns_ieraksts])], ignore_index=True)
            df_jauns.to_csv(DATU_FAILS, index=False, encoding="utf-8")
            st.success(f"✅ Saglabāts! {vards} {uzvards} ({klase}) — {kopa} punkti, balle {balle}")
            st.balloons()

# =============================================================
# LAPA 2: SKATĪT DATUS
# =============================================================
elif lapa == "📊 Skatīt datus":
    st.title("📊 Visi ZPD vērtējumi")
    df = ieladet_datus()
    
    if len(df) == 0:
        st.warning("Datu nav! Vispirms ievadi vērtējumus.")
    else:
        st.markdown(f"**Kopā failā:** {len(df)} skolēni")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filtrs_gads = st.multiselect("Mācību gads", 
                                         options=sorted(df["Mācību gads"].unique()),
                                         default=sorted(df["Mācību gads"].unique()))
        with col2:
            filtrs_klase = st.multiselect("Klase", 
                                          options=sorted(df["Klase"].unique()),
                                          default=sorted(df["Klase"].unique()))
        with col3:
            filtrs_balle = st.slider("Minimālā balle", 1, 10, 1)
        
        df_filtr = df[
            (df["Mācību gads"].isin(filtrs_gads)) &
            (df["Klase"].isin(filtrs_klase)) &
            (df["Balle"] >= filtrs_balle)
        ]
        st.markdown(f"**Atbilst filtram:** {len(df_filtr)} skolēni")
        st.dataframe(df_filtr, use_container_width=True, height=500)

# =============================================================
# LAPA 3: STATISTIKA UN TOP 10
# =============================================================
elif lapa == "📈 Statistika un TOP 10":
    st.title("📈 Statistika un TOP 10 uz novadu")
    df = ieladet_datus()
    
    if len(df) == 0:
        st.warning("Datu nav! Vispirms ievadi vērtējumus.")
    else:
        st.subheader("📊 Vispārējā statistika")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Skolēni kopā", len(df))
        col2.metric("Vidējā balle", f"{df['Balle'].mean():.2f}")
        col3.metric("Augstākie p.", f"{df['Kopā'].max():.0f}")
        col4.metric("Zemākie p.", f"{df['Kopā'].min():.0f}")

        st.markdown("---")
        st.subheader("🏆 TOP 10 uz novada konkursu (balle ≥ 8, 2025/2026)")
        top10 = df[(df["Mācību gads"] == "2025/2026") & (df["Balle"] >= 8)]
        top10 = top10.sort_values("Kopā", ascending=False).head(10)
        if len(top10) > 0:
            st.dataframe(top10[["Vārds", "Uzvārds", "Klase", "Kopā", "Balle"]], 
                        use_container_width=True)
        else:
            st.info("Pagaidām nav skolēnu, kas atbilst kritērijiem.")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Balles sadalījums")
            fig, ax = plt.subplots(figsize=(8, 5))
            balles_count = df["Balle"].value_counts().sort_index()
            ax.bar(balles_count.index, balles_count.values, color="steelblue", edgecolor="black")
            ax.set_xlabel("Balle")
            ax.set_ylabel("Skolēnu skaits")
            ax.set_xticks(range(1, 11))
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig)
        with col2:
            st.subheader("📈 Vidējā balle pa gadiem")
            fig, ax = plt.subplots(figsize=(8, 5))
            vid_gadi = df.groupby("Mācību gads")["Balle"].mean()
            ax.bar(vid_gadi.index, vid_gadi.values, color="coral", edgecolor="black")
            ax.set_ylabel("Vidējā balle")
            ax.set_ylim(0, 10)
            for i, v in enumerate(vid_gadi.values):
                ax.text(i, v + 0.1, f"{v:.2f}", ha="center", fontweight="bold")
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig)

        st.markdown("---")
        st.subheader("🏫 Statistika pa klasēm")
        stat_klases = df.groupby("Klase").agg(
            Skolēni=("Vārds", "count"),
            Vidējā_balle=("Balle", "mean"),
            Vidējie_punkti=("Kopā", "mean")
        ).round(2)
        st.dataframe(stat_klases, use_container_width=True)

        # =============================================================
        # 🤖 AI ANALĪZE — JAUNĀ SADAĻA
        # =============================================================
        st.markdown("---")
        st.subheader("🤖 AI analīze")
        st.markdown("Nospied pogu, lai saņemtu automātisku AI komentāru par ZPD rezultātiem.")

        if st.button("🔍 Analizēt ar AI", type="primary", use_container_width=True):
            with st.spinner("AI analizē datus... ⏳"):
                rezultats = ai_analize(df)
            st.success("✅ Analīze gatava!")
            st.markdown(rezultats)