import streamlit as st
import pandas as pd
import numpy as np

logo = st.sidebar.image('img/logo_chm.png')
st.sidebar.caption("Guide d'analyse pharmacothérapeutique chez le patient MUPA.")

data_frame = pd.read_csv('Tableau Medoc Source Code.csv')
data_frame.set_index('Index', inplace=True)

liste_medoc = [str(medoc) for medoc in set(data_frame.index)]
liste_medoc.sort()

col1, col2 = st.columns(2)
col1.subheader('Liste des prescriptions')
col2.subheader('Commentaires à adapter')

option = st.sidebar.selectbox(
     "Choisis un médicament. Petite astuce : Il suffit de cliquer sur la barre de recherche (pas besoin d'effacer) et de taper les première lettres du"
     " médicament (DCI ou Princeps).",
     liste_medoc)

if "liste_presc" in st.session_state:
     liste_presc = st.session_state.liste_presc

if "liste_presc" not in st.session_state:
     liste_presc = []

if st.sidebar.button("Ajouter le médicament"):
     liste_presc.append(option)
     st.session_state.liste_presc = liste_presc

if st.sidebar.button("Réinitialiser la prescritpion"):
     if 'liste_presc' in st.session_state:
            del st.session_state.liste_presc
               
if "liste_presc" in st.session_state:
     for medoc in st.session_state.liste_presc :  
          col1, col2 = st.columns(2)
          col1.write(medoc)
          with col2 :
               with st.expander("Commentaires"):                                  
                    compteur = 0
                    for i in data_frame.index: 
                        if i == medoc:
                            compteur += 1

                    for i in range(compteur):
                        txt = st.text_area(f"{data_frame.loc[{medoc}, 'Condition'][i]}",
                                           f"{data_frame.loc[{medoc}, 'Paragraphe'][i]}",
                                           key = int(np.random.randint(0, 100000, size=(1, 1))), max_chars=500) 

st.write(" ----------------------------- ")                
                    
anticho_periph_num = []
anticho_periph_name = []
anticho_central_num = []
anticho_central_name = []
torsadogene_num = []
torsadogene_name = []
hypok_num = []
hypok_name = []
hyperk_num = []
hyperk_name = []
depresseur_SNC_num = []
depresseur_SNC_name = []
medoc_inaprop_num = []
medoc_inaprop_name = []
bradycardi_num = []
bradycardi_name = []
hypoT_ortho_num = []
hypoT_ortho_name = []
pro_convuls_num = []
pro_convuls_name = []
                    
if "liste_presc" in st.session_state:
     for medoc in st.session_state.liste_presc :
          if data_frame.loc[{medoc}, 'Charge anticholinergique périphérique'][0] > 0 :
               anticho_periph_num.append(int(data_frame.loc[{medoc}, 'Charge anticholinergique périphérique'][0]))
               anticho_periph_name.append(medoc)
          if data_frame.loc[{medoc}, 'Charge anticholinergique centrale'][0] > 0 :
               anticho_central_num.append(int(data_frame.loc[{medoc}, 'Charge anticholinergique centrale'][0]))
               anticho_central_name.append(medoc)
          if data_frame.loc[{medoc}, 'Torsadogène'][0] == 1 :
               torsadogene_num.append(int(data_frame.loc[{medoc}, 'Torsadogène'][0]))
               torsadogene_name.append(medoc)
          if data_frame.loc[{medoc}, 'Hypok'][0] == 1 :
               hypok_num.append(int(data_frame.loc[{medoc}, 'Hypok'][0]))
               hypok_name.append(medoc)
          if data_frame.loc[{medoc}, 'HyperK'][0] == 1 :
               hyperk_num.append(int(data_frame.loc[{medoc}, 'HyperK'][0]))
               hyperk_name.append(medoc)
          if data_frame.loc[{medoc}, 'Dépresseur_SNC'][0] == 1 :
               depresseur_SNC_num.append(int(data_frame.loc[{medoc}, 'Dépresseur_SNC'][0]))
               depresseur_SNC_name.append(medoc)
          if data_frame.loc[{medoc}, 'Médicam inapprop'][0] == 1 :
               medoc_inaprop_num.append(int(data_frame.loc[{medoc}, 'Médicam inapprop'][0]))
               medoc_inaprop_name.append(medoc)
          if data_frame.loc[{medoc}, 'HypoT_Ortho'][0] == 1 :
               hypoT_ortho_num.append(int(data_frame.loc[{medoc}, 'HypoT_Ortho'][0]))
               hypoT_ortho_name.append(medoc)
          if data_frame.loc[{medoc}, 'Pro_convul'][0] == 1 :
               pro_convuls_num.append(int(data_frame.loc[{medoc}, 'Pro_convul'][0]))
               pro_convuls_name.append(medoc)
     
     if np.sum(anticho_periph_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Charge anticholinergique périphérique de cette prescription : {np.sum(anticho_periph_num)}")
          with col2 :
               with st.expander("Médicament(s) anticholinergique(s) de la prescription"):
                    for name in anticho_periph_name : 
                         st.write(f"\n {name}")
     if np.sum(anticho_central_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Charge anticholinergique centrale de cette prescription : {np.sum(anticho_central_num)}")
          with col2 :
               with st.expander("Médicament(s) anticholinergique(s) avec action central dans cette prescription"):
                    for name in anticho_central_name : 
                         st.write(f"\n {name}")
     if np.sum(torsadogene_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament torsadogène dans cette prescription : {np.sum(torsadogene_num)}")
          with col2 :
               with st.expander("Médicament(s) torsadogène(s) de la prescription"):
                    for name in torsadogene_name : 
                         st.write(f"\n {name}")
     if np.sum(hypok_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament hypokaliémiant dans cette prescription : {np.sum(hypok_num)}")
          with col2 :
               with st.expander("Médicament(s) hypokaliémiant(s) de la prescription"):
                    for name in hypok_name : 
                         st.write(f"\n {name}")
     if np.sum(hyperk_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament hyperkaliémiant dans cette prescription : {np.sum(hyperk_num)}")
          with col2 :
               with st.expander("Médicament(s) hyperkaliémiant(s) de la prescription"):
                    for name in hyperk_name : 
                         st.write(f"\n {name}")                
     if np.sum(depresseur_SNC_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament dépresseur du système nerveux central dans cette prescription : {np.sum(depresseur_SNC_num)}")
          with col2 :
               with st.expander("Médicament(s) dépresseur(s) du système nerveux central de la prescription"):
                    for name in depresseur_SNC_name : 
                         st.write(f"\n {name}")
     if np.sum(medoc_inaprop_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament potentiellement inapproprié chez la personne âgée dans cette prescription : {np.sum(medoc_inaprop_num)}")
          with col2 :
               with st.expander("Médicament(s) potentiellement inapproprié(s) chez la personne âgée de la prescription"):
                    for name in medoc_inaprop_name : 
                         st.write(f"\n {name}")
     if np.sum(hypoT_ortho_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament à l'origine d'hypotension (hors antihypertenseur), notamment orthostatique, dans cette prescription : {np.sum(hypoT_ortho_num)}")
          with col2 :
               with st.expander("Médicament(s) à l'origine d'hypotension (hors antihypertenseur), notamment orthostatique, de la prescription"):
                    for name in hypoT_ortho_name : 
                         st.write(f"\n {name}")
     if np.sum(pro_convuls_num) > 0 :
          col1, col2 = st.columns(2)
          col1.write(f"Nombre de médicament proconvulsivant dans cette prescription : {np.sum(pro_convuls_num)}")
          with col2 :
               with st.expander("Médicament(s) proconvulsivant(s) de la prescription"):
                    for name in pro_convuls_name : 
                         st.write(f"\n {name}")
