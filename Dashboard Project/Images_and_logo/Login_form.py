import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader


names = ["Emmanuel Bolaji", "Miracle Ayodeji", "Anita Smiles"]
usernames = ["Bolajiemmanuel01", "Miraayo", "Ants1"]

file_path = Path(__file__).parent / "Images_and_logo/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)


with open('Images_and_logo/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == "False":
    st.error("🚨 Username/Password is incorrect 🚨")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    pass
