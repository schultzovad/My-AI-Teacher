import streamlit as st
from supabase import create_client

# Toto načíta kľúče z "Secrets" v Streamlit Cloud
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)
