import streamlit as st
import datetime
import pandas as pd

# Oldal konfiguráció
st.set_page_config(page_title="CT Effektív Dózis Kalkulátor", page_icon="??", layout="centered")

st.title("?? CT Effektív Dózis Kalkulátor")
st.markdown("Számítsd ki gyorsan a CT vizsgálatok effektív dózisát (DLP alapján) az ICRP 103 szabvány szerint[cite: 1].")

# Standard ICRP 103 / AAPM felnõtt k-tényezõk (mSv / (mGy * cm))[cite: 1]
K_FACTORS = {
    "Egész test / Általános (0.015)": 0.015,
    "Has - Kismedence (0.015)": 0.015,
    "Mellkas - Has - Kismedence (0.015)": 0.015,
    "Mellkas (0.014)": 0.014,
    "Nyak (0.0059)": 0.0059,
    "Koponya (0.0021)": 0.0021
}

# Beviteli mezõk a felületen
col1, col2 = st.columns(2)

with col1:
    ctdi_szoveg = st.text_input("CTDIvol (mGy):", "10.0")[cite: 1]
with col2:
    dlp_szoveg = st.text_input("DLP (mGy*cm):", "500")[cite: 1]

# Anatómiai régió választó
regio_nev = st.selectbox("Anatómiai régió (k):", list(K_FACTORS.keys()))[cite: 1]

# Egyedi k-tényezõ opció
egyedi_aktiv = st.checkbox("Egyedi k-tényezõ megadása")[cite: 1]
if egyedi_aktiv:
    k_ertek = st.number_input("Egyedi k-érték:", value=0.015, format="%.5f")[cite: 1]
    regio_nev = "Egyedi k-tényezõ"[cite: 1]
else:
    k_ertek = K_FACTORS[regio_nev][cite: 1]

# Számítás gomb
if st.button("Kiszámítás", type="primary"):
    try:
        dlp_ertek = float(dlp_szoveg)
        ctdi_ertek = float(ctdi_szoveg) if ctdi_szoveg else 0.0
        
        if dlp_ertek < 0 or ctdi_ertek < 0:
            st.error("Az értékek nem lehetnek negatívak!")[cite: 1]
        else:
            # Effektív dózis számítás[cite: 1]
            effektiv_dozis = k_ertek * dlp_ertek
            
            # Eredmény megjelenítése
            st.success(f"**Számított effektív dózis (E):** {effektiv_dozis:.3f} mSv")[cite: 1]
            st.info(f"CTDIvol: {ctdi_ertek} mGy | DLP: {dlp_ertek} mGy*cm (k-tényezõ: {k_ertek} mSv/(mGy*cm))")[cite: 1]
            
            # Adatok tárolása a letöltéshez
            adat = [{
                "Datum_Ido": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),[cite: 1]
                "Regio_k": regio_nev,[cite: 1]
                "k_tenyezo_mSv_mGycm": str(k_ertek).replace(".", ","),[cite: 1]
                "CTDIvol_mGy": str(ctdi_ertek).replace(".", ","),[cite: 1]
                "DLP_mGycm": str(dlp_ertek).replace(".", ","),[cite: 1]
                "Effektiv_dozis_mSv": f"{effektiv_dozis:.3f}".replace(".", ",")[cite: 1]
            }]
            df = pd.DataFrame(adat)
            
            # CSV letöltõ gomb
            csv_data = df.to_csv(index=False, sep=";").encode("cp1252", errors="ignore")
            st.download_button(
                label="?? Eredmény mentése CSV-be",
                data=csv_data,
                file_name="ct_dozis_eredmeny.csv",
                mime="text/csv"
            )
            
    except ValueError:
        st.error("Kérlek érvényes számokat adj meg!")[cite: 1]
