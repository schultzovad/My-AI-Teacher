# 1. Získanie jazyka z URL (ak tam nie je, nastaví SK)
query_params = st.query_params
url_lang = query_params.get("lang", "SK") 

# 2. Kontrola, či je jazyk v našom zozname (prevencia chýb)
if url_lang not in lang_data:
    url_lang = "SK"

# 3. Nastavenie textov podľa jazyka z URL
t = lang_data[url_lang]

# Sidebar teraz nechaj prázdny (alebo tam daj len info text)
# Ak chceš šípku zachovať, musíš tam nechať aspoň prázdny sidebar:
with st.sidebar:
    st.write(f"🌐 {url_lang}")
