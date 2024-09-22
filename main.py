import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

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
