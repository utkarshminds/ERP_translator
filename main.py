import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

import hmac



def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()


# Sample DataFrame (you can replace this with the real data from the image)
data = {
    'Item number': ['MI65789', 'MI65794', 'MI65797','MI1','MI2'],
    'Name': ['AMX 3033GM-BL', 'CON-SNT-IE4000BT', 'CON-SNT-CBS25U08','DUMMY','DUMMY2'],
    'Description': ['DECORA FACEPLATE 3 GANG BLACK', '8X SFP 10/100M, 4X1G LAN B', 'POWER CONN FOR GE, PAR L POE','Chair','Elevator']
}

df = pd.DataFrame(data)

# Streamlit app
st.title("Data Display with Language Translation")

# Language selection
language = st.radio("Choose Language", ('English', 'French'))

def translate_dataframe(df, target_language):
    """Translate all text columns of the DataFrame to the target language."""
    df_translated = df.copy()
    for col in df.columns:
        df_translated[col] = df[col].apply(lambda x: GoogleTranslator(source='auto', target=target_language).translate(x))
    return df_translated

# Show DataFrame based on language selection
if language == 'French':
    df_translated = translate_dataframe(df, 'fr')
    st.dataframe(df_translated)
else:
    st.dataframe(df)
