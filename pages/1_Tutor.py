import streamlit as st
import sys
import os

# Toto zabezpečí, že sa kód v 'pages' vie pozrieť o úroveň vyššie do hlavného priečinka
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_utils import get_db, hash_pwd

# --- A SEM POD TOTO VLOŽ SVOJ PÔVODNÝ KÓD TÚTORA ---
st.title("AI Tútor")
