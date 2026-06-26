import streamlit as st
from supabase import create_client

# Tieto kľúče máš v Streamlit Secrets
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
