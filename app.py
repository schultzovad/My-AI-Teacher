import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. NASTAVENIE STRÁNKY
st.set_page_config(page_title="AI Doučovateľ", layout="centered")

# 2. BEZPEČNÉ NAČÍTANIE API KĽÚČA
# Kľúč vložíš v Streamlite do Settings -> Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Chýba API kľúč! Prosím, vlož ho do Secrets v Streamlit nastaveniach.")

model = genai.GenerativeModel('gemini-1.5-flash')

# 3. DIZAJN APLIKÁCIE
st.title("📚 Tvoj AI Doučovateľ")
st.subheader("Nahraj fotku a ja ti učivo vysvetlím!")

# Pole na nahranie súboru
uploaded_file = st.file_uploader("Vyber fotku poznámok (JPG, PNG) alebo PDF...", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    # Zobrazenie nahranej fotky
    image = Image.open(uploaded_file)
    st.image(image, caption='Tvoje poznámky sú nahrané!', use_column_width=True)
    
    # Tlačidlo na spustenie analýzy
    if st.button('✨ Vysvetli mi to ľudsky'):
        
        # Inštrukcia pre AI (Prompt)
        prompt = """
        Si priateľský a trpezlivý učiteľ, ktorý chce študentovi pomôcť pochopiť učivo. 
        Pozri sa na tento obrázok/dokument a urob nasledujúce:
        1. Stručne zhrň, o čom sú tieto poznámky.
        2. Vysvetli hlavné pojmy a tému tak, aby to pochopil aj niekto, kto na hodine chýbal.
        3. Ak je tam niečo zložité, použi príklad zo života.
        4. Na záver pridaj 3 krátke kontrolné otázky, aby si študent overil, či to pochopil.
        
        Odpovedaj v slovenskom jazyku, prehľadne (používaj odrážky a tučné písmo).
        """
        
        with st.spinner('Daj mi chvíľku, čítam tvoje poznámky...'):
            try:
                # Odoslanie obrázka do AI
                response = model.generate_content([prompt, image])
                
                # Zobrazenie výsledku
                st.success("Hotovo! Tu je tvoj výklad:")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ups, niečo sa nepodarilo: {e}")

# Päta aplikácie
st.markdown("---")
st.caption("Vytvorené pre tvoj lepší prospech 🎓")
