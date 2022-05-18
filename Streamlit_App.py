import streamlit as st
import pandas as pd

logo = st.sidebar.image('img/logo_chm.png')
st.sidebar.caption("Guide d'analyse pharmacothérapeutique chez le patient MUPA.")
st.subheader('À adapter selon le contexte')

data_frame = pd.read_csv('Analyse Pharmacotherapeutique File.csv')
data_frame.set_index('Index', inplace=True)

option = st.sidebar.selectbox(
     'Choisis un médicament',
     set(data_frame.index))

st.sidebar.write('Tu as sélectionné:', option)

compteur = 0
for i in data_frame.index: 
    if i == option:
        compteur += 1

for i in range(compteur):
    txt = st.text_area(f"{data_frame.loc[{option}, 'Condition'][i]}", f"{data_frame.loc[{option}, 'Paragraphe'][i]}", max_chars=500)
