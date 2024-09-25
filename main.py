import streamlit as st
import pandas as pd
import deepl  # Import the deepl library
import hmac
import numpy as np
# DeepL API key (use your actual API key)
DEEPL_API_KEY = st.secrets["DEEPL_API_KEY"]["DEEPL_API_KEY"]  # Replace with your DeepL API key
translator = deepl.Translator(DEEPL_API_KEY)

# Function to check username and password
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
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(
            st.session_state["password"], st.secrets.passwords[st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

# Stop execution if password is incorrect
if not check_password():
    st.stop()

# Create two tabs
tab1, tab2 = st.tabs(["Item Master Translation", "Demo Translation"])

# Tab 1: Item Master Translation
with tab1:
    st.title("GFT Item Master")

    # Read data from the uploaded template file
    df = pd.read_excel("Template_with_dummy_data.xlsx")
    print(df.columns)
    df = df[["Itp","Item number","name","description","Sts","Item grp","U/M","P grp","Quality gr","Resp"]]

    # Filters: LTP and Item number
    st.subheader("Filter Data")
    ltp_filter = st.text_input("Filter by LTP")
    item_filter = st.text_input("Filter by Item number")

    # Apply filters
    if ltp_filter:
        df = df[df['LTP'].astype(str).str.contains(ltp_filter, case=False, na=False)]
    if item_filter:
        df = df[df['Item number'].astype(str).str.contains(item_filter, case=False, na=False)]

    # Show the filtered data
    st.dataframe(df)

    # Language options
    languages = ['English', 'French', 'Spanish', 'German', 'Japanese', 'Dutch', 'Portuguese', 'Italian']
    language = st.radio("Choose Language", languages)

    # Function to translate filtered DataFrame using DeepL API
    def translate_to_language(df, target_language):
        df_translated = df.copy()

        # Function to check if a value is translatable (i.e., non-null and a string)
        def translate_value(value):
            if pd.notnull(value) and isinstance(value, str):
                return translator.translate_text(value, target_lang=target_language).text
            return value  # Return the original value if it's NaN, None, or numeric

        # Apply the translation function to each column
        for col in df.columns:
            df_translated[col] = df[col].apply(translate_value)

        return df_translated

    # Language codes for translation
    language_codes = {
        'English': 'EN-US',
        'French': 'FR',
        'Spanish': 'ES',
        'German': 'DE',
        'Japanese': 'JA',
        'Dutch': 'NL',
        'Portuguese': 'PT',
        'Italian': 'IT'
    }

    # Add a button to trigger translation (with unique key)
    if st.button("Translate", key="translate_item_master"):
        if language != 'English':
            df_translated = translate_to_language(df, language_codes[language])
            st.dataframe(df_translated)
        else:
            st.dataframe(df)

# Tab 2: Demo Translation from English to German
with tab2:
    st.title("CRS630 - Accounting Identity - Open ")

    # Read the demo document (Demo.xlsx)
    df_demo = pd.read_excel("Demo.xlsx", header=0, skiprows=2, nrows=25, usecols=[0,1,2,3,4,5,6,7,8,9,10])

    df_demo = df_demo.iloc[0:]

    # Filter by Actng ID
    actng_id_filter = st.text_input("Filter by Actng ID")

    # Apply filter
    if actng_id_filter:
        df_demo = df_demo[df_demo['Actng ID'].astype(str).str.contains(actng_id_filter, case=False, na=False)]

    # Show the filtered data
    st.dataframe(df_demo)

    # Add two radio buttons for English and German
    language_demo = st.radio("Select Language", ["English", "German"], key="demo_language")

    # Function to translate filtered data using DeepL API


    def translate_to_language(df, target_language):
        df_translated = df.copy()

        # Function to check if a value is translatable (i.e., non-null and a string)
        def translate_value(value):
            if pd.notnull(value) and isinstance(value, str):
                return translator.translate_text(value, target_lang=target_language).text
            return value  # Return the original value if it's NaN, None, or numeric

        # Apply the translation function to each column
        for col in df.columns:
            df_translated[col] = df[col].apply(translate_value)

        return df_translated


    # Add a button to trigger translation after language is selected (with unique key)
    if st.button("Translate", key="translate_demo"):
        if language_demo == "German":
            df_demo_translated = translate_to_language(df_demo, "DE")
            st.dataframe(df_demo_translated)
        elif language_demo == "English":
            df_demo_translated = translate_to_language(df_demo, "EN-US")
            st.dataframe(df_demo_translated)    
        else:
            st.dataframe(df_demo)  # Show data as it is
