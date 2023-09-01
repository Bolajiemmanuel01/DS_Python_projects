import pickle
from pathlib import Path
import streamlit_authenticator as stauth
#
# names = ["Emmanuel Bolaji", "Miracle Ayodeji", "Anita Smiles"]
# usernames = ["Bolajiemmanuel01", "Miraayo", "Ants1"]
# passwords = ["abc123", "def456", "ghi789"]
#
# hashed_passwords = stauth.Hasher(passwords).generate()
#
# file_path = Path(__file__).parent / "Images_and_logo/hashed_pw.pkl"
# with file_path.open("wb") as file:
#     pickle.dump(hashed_passwords, file)
hashed_passwords = stauth.Hasher(["abc123", "def456", "ghi789"]).generate()
print(hashed_passwords)


