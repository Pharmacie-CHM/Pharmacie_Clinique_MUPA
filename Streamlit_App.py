import streamlit as st
import pandas as pd
import numpy as np
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from streamlit.logger import get_logger
from english_version import App_English_Version

LOGGER = get_logger(__name__)

def main():
    st.set_page_config(
        page_title="CheckDrugs",
        page_icon="💊",
        layout="wide"
    )
    logo = st.sidebar.image('logo_chm.png')
    pages = ("🇫🇷 Version Française", "🇬🇧 English Version")
    page = st.sidebar.selectbox(label = "For the English version ↙️",
                                options = pages,
                                index = 0,
                                )

    #padding = 0
    #st.markdown(f""" <style>
    #    .reportview-container .main .block-container{{
    #        padding-top: {padding}rem;
    #        padding-right: {padding}rem;
    #        padding-left: {padding}rem;
    #        padding-bottom: {padding}rem;
    #    }} </style> """, unsafe_allow_html=True)

    if page == "🇬🇧 English Version":
        App_English_Version.run()
    else :
        def run():
            data_frame = pd.read_csv('Analyse Pharmacotherapeutique File.csv')
            data_frame.set_index('Index', inplace=True)

            liste_medoc = [str(medoc) for medoc in set(data_frame.index)]
            liste_medoc.sort()

            option = st.sidebar.selectbox(
                  "Choisis un médicament. Petite astuce : Il suffit de cliquer sur la barre de recherche (pas besoin d'effacer) et de taper les première lettres du"
                  " médicament (DCI ou Princeps).",
                  liste_medoc)

            if "liste_presc" in st.session_state:
                  liste_presc = st.session_state.liste_presc

            if "liste_presc" not in st.session_state:
                  liste_presc = []

            if st.sidebar.button("Ajouter le médicament"):
                  if option == "# Choisir un médicament" :
                        st.error("ERROR : Vous devez selectionner un médicament avant d'appuyer sur le bouton 'Ajouter le médicament'.")
                  elif option not in liste_presc:
                       liste_presc.append(option)
                       st.session_state.liste_presc = liste_presc
                  else :
                       st.error("ERROR : Tu ne peux pas ajouter deux fois le même médicament dans la liste des prescriptions !")

            if st.sidebar.button("Retirer le médicament"):
                  try : 
                       liste_presc.remove(option)
                       st.session_state.liste_presc = liste_presc
                  except ValueError :
                       st.error("ERROR : Tu ne peux pas retirer des prescriptions un médicament qui n'est pas déjà dans les prescriptions !")
                        
            if st.sidebar.button("Réinitialiser la liste des prescriptions"):
                  if 'liste_presc' in st.session_state:
                         del st.session_state.liste_presc

            st.header('Analyse pharmaco-thérapeutique')
            st.subheader('Liste des prescriptions')
            
            if liste_presc == [] :
                st.image('Tutoriel.png')
            
            if "liste_presc" in st.session_state:
                 for medoc in st.session_state.liste_presc :  
                      col1, col2 = st.columns([1, 3])
                      col1.write(medoc)
                      with col2 :
                           with st.expander("Analyse de la prescription"):                                  
                                compteur = 0
                                for i in data_frame.index: 
                                    if i == medoc:
                                        compteur += 1

                                compteur2 = 0
                                for i in range(compteur):
                                     if data_frame.loc[{medoc}, 'Category'][i] == 'Contrôle des indications :' :
                                          compteur2 += 1
                                for i in range(compteur):
                                     if i == 0 :
                                          if compteur2 == 1 :
                                              st.write(f"**{data_frame.loc[{medoc}, 'Category'][i]}**")
                                              st.text_area(f"{data_frame.loc[{medoc}, 'Condition'][i]}",
                                                       f"{data_frame.loc[{medoc}, 'Paragraphe'][i]}",
                                                       key = int(np.random.randint(0, 100000, size=(1, 1))),
                                                       max_chars=500, help=f"Source : {data_frame.loc[{medoc}, 'Reference'][i]}")
                                              text_to_be_copied = data_frame.loc[{medoc}, 'Paragraphe'][i]
                                              copy_dict = {"content": text_to_be_copied}

                                              copy_button = Button(label="Copier le texte")
                                              copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
                                                   navigator.clipboard.writeText(content);
                                                   """))

                                              no_event = streamlit_bokeh_events(
                                                   copy_button,
                                                   events="GET_TEXT",
                                                   key=int(np.random.randint(0, 100000, size=(1, 1))),
                                                   refresh_on_update=True,
                                                   override_height=40,
                                                   debounce_time=0)

                                          else :
                                            st.write(f"**{data_frame.loc[{medoc}, 'Category'][i]}**")
                                            txt = st.checkbox(f"{data_frame.loc[{medoc}, 'Condition'][i]}",
                                                              key = medoc + data_frame.loc[{medoc}, 'Condition'][i])
                                            if txt :
                                                st.text_area("À adapter selon le contexte", 
                                                              f"{data_frame.loc[{medoc}, 'Paragraphe'][i]}",
                                                              key = int(np.random.randint(0, 100000, size=(1, 1))),
                                                              max_chars=500, help=f"Source : {data_frame.loc[{medoc}, 'Reference'][i]}")
                                                text_to_be_copied = data_frame.loc[{medoc}, 'Paragraphe'][i]
                                                copy_dict = {"content": text_to_be_copied}

                                                copy_button = Button(label="Copier le texte")
                                                copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
                                                    navigator.clipboard.writeText(content);
                                                    """))

                                                no_event = streamlit_bokeh_events(
                                                    copy_button,
                                                    events="GET_TEXT",
                                                    key=int(np.random.randint(0, 100000, size=(1, 1))),
                                                    refresh_on_update=True,
                                                    override_height=40,
                                                    debounce_time=0)
                                     else :
                                        #try :
                                        if data_frame.loc[{medoc}, 'Category'][i] != data_frame.loc[{medoc}, 'Category'][i-1] :
                                             st.write(" ----------------------------- ") 
                                             st.write(f"**{data_frame.loc[{medoc}, 'Category'][i]}**")
                                        txt = st.checkbox(f"{data_frame.loc[{medoc}, 'Condition'][i]}",
                                                         key = medoc + data_frame.loc[{medoc}, 'Condition'][i])
                                        #except :
                                        #st.error("ERROR : La base de données interne contient un duplicat (Nom de médicament + Condition). À corriger")
                                        if txt :                
                                            st.text_area("À adapter selon le contexte", 
                                                        f"{data_frame.loc[{medoc}, 'Paragraphe'][i]}",
                                                        key = int(np.random.randint(0, 100000, size=(1, 1))),
                                                        max_chars=500, help=f"Source : {data_frame.loc[{medoc}, 'Reference'][i]}")
                                            text_to_be_copied = data_frame.loc[{medoc}, 'Paragraphe'][i]
                                            copy_dict = {"content": text_to_be_copied}

                                            copy_button = Button(label="Copier le texte")
                                            copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
                                                navigator.clipboard.writeText(content);
                                                """))

                                            no_event = streamlit_bokeh_events(
                                                copy_button,
                                                events="GET_TEXT",
                                                key=int(np.random.randint(0, 100000, size=(1, 1))),
                                                refresh_on_update=True,
                                                override_height=40,
                                                debounce_time=0)  

                      if data_frame.loc[{medoc}, 'Inducteur_enz'][0] == 1 :
                           col1.warning("Inducteur enzymatique puissant")
                           with col2 :
                                with st.expander("Recommandation"):
                                     st.write("""
                      Nous recommandons de vérifier la présence d'intéraction médicamenteuse entre chaque médicament et l'inducteur enzymatique 
                      à l'aide du détecteur d'intéraction médicamenteuse du Vidal ou de la dernière version récente du Thésaurus de l'ANSM (en s'assurant de vérifier
                      à la fois dans la partie "Anticonvulsivant inducteur enzymatique" mais aussi dans la partie propre du médicamennt inducteur enzymatique concerné).
                  """)

            anticholinergics_num = []
            anticholinergics_name = []
            anticholinergics_cent_num = []
            anticholinergics_cent_name = []
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
            hypoglycemia_num = []
            hypoglycemia_name = []
    
            if "liste_presc" in st.session_state :
                for medoc in st.session_state.liste_presc :
                      if data_frame.loc[{medoc}, 'Anticholinergics'][0] > 0 :
                           anticholinergics_num.append(int(data_frame.loc[{medoc}, 'Anticholinergics'][0]))
                           anticholinergics_name.append(medoc)
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
                      if data_frame.loc[{medoc}, 'Bradycardisant'][0] == 1 :
                           bradycardi_num.append(int(data_frame.loc[{medoc}, 'Bradycardisant'][0]))
                           bradycardi_name.append(medoc)
                      if data_frame.loc[{medoc}, 'HypoT_Ortho'][0] == 1 :
                           hypoT_ortho_num.append(int(data_frame.loc[{medoc}, 'HypoT_Ortho'][0]))
                           hypoT_ortho_name.append(medoc)
                      if data_frame.loc[{medoc}, 'Pro_convul'][0] == 1 :
                           pro_convuls_num.append(int(data_frame.loc[{medoc}, 'Pro_convul'][0]))
                           pro_convuls_name.append(medoc)
                      if data_frame.loc[{medoc}, 'Anticholinergic_Central'][0] == 1 :
                           anticholinergics_cent_num.append(int(data_frame.loc[{medoc}, 'Anticholinergic_Central'][0]))
                           anticholinergics_cent_name.append(medoc)
                      if data_frame.loc[{medoc}, 'Hypoglycemia'][0] == 1 :
                           hypoglycemia_num.append(int(data_frame.loc[{medoc}, 'Hypoglycemia'][0]))
                           hypoglycemia_name.append(medoc)

                st.write(" ----------------------------- ")   

                if np.sum(medoc_inaprop_num) > 0 :
                    col1, col2 = st.columns(2)
                    col1.write(f"Nombre de médicament **potentiellement inapproprié chez la personne âgée** dans ce bilan médicamenteux : {np.sum(medoc_inaprop_num)}")
                    with col2 :
                        with st.expander("Médicament(s) potentiellement inapproprié(s) chez la personne âgée du bilan médicamenteux"):
                            for name in medoc_inaprop_name :
                                st.write(f"\n {name}")

                if np.sum(hypoT_ortho_num) > 0 or np.sum(depresseur_SNC_num) > 0 or np.sum(hypoglycemia_num) > 0 :
                    st.write(" ----------------------------- ") 
                    st.write("**Analyse du risque de chute :**")

                    if np.sum(hypoT_ortho_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **à l'origine d'hypotension** (hors antihypertenseur), notamment orthostatique, dans ce bilan médicamenteux : {np.sum(hypoT_ortho_num)}")
                        with col2 :
                            with st.expander("Médicament(s) à l'origine d'hypotension (hors antihypertenseur), notamment orthostatique, du bilan médicamenteux"):
                                for name in hypoT_ortho_name : 
                                    st.write(f"\n {name}") 

                    if np.sum(depresseur_SNC_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **à l'origine d'une altération de l'équilibre** dans ce bilan médicamenteux : {np.sum(depresseur_SNC_num)}")
                        with col2 :
                            with st.expander("Médicament(s) à l'origine d'une altération de l'équilibre du bilan médicamenteux"):
                                for name in depresseur_SNC_name : 
                                    st.write(f"\n {name}")   
                   
                    if np.sum(hypoglycemia_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **hypoglycémiant** dans ce bilan médicamenteux : {np.sum(hypoglycemia_num)}")
                        with col2 :
                            with st.expander("Médicament(s) hypoglycémiant(s) du bilan médicamenteux"):
                                for name in hypoglycemia_name : 
                                    st.write(f"\n {name}")
                    

                if np.sum(anticholinergics_cent_num) > 0 or np.sum(depresseur_SNC_num) > 0 :
                    st.write(" ----------------------------- ") 
                    st.write("**Analyse du risque de troubles confusionnelles ou de désorientation :**")

                    if np.sum(anticholinergics_cent_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **anticholinergique central** de ce bilan médicamenteux : {np.sum(anticholinergics_cent_num)}")
                        with col2 :
                            with st.expander("Médicament(s) anticholinergique(s) central/centraux du bilan médicamenteux"):
                                for name in anticholinergics_cent_name : 
                                    st.write(f"\n {name}")

                    if np.sum(depresseur_SNC_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **dépresseur du système nerveux central** dans ce bilan médicamenteux : {np.sum(depresseur_SNC_num)}")
                        with col2 :
                            with st.expander("Médicament(s) dépresseur(s) du système nerveux central du bilan médicamenteux"):
                                for name in depresseur_SNC_name : 
                                    st.write(f"\n {name}") 

                if np.sum(torsadogene_num) > 0 or np.sum(bradycardi_num) > 0 or np.sum(hypok_num) > 0 :
                    st.write(" ----------------------------- ") 
                    st.write("**Analyse du risque d'arythmie cardiaque de type torsade de pointes :**")

                    if np.sum(torsadogene_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **torsadogène** dans ce bilan médicamenteux : {np.sum(torsadogene_num)}")
                        with col2 :
                            with st.expander("Médicament(s) torsadogène(s) du bilan médicamenteux"):
                                for name in torsadogene_name :
                                    st.write(f"\n {name}")
                    if np.sum(bradycardi_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **bradycardisant** dans ce bilan médicamenteux : {np.sum(bradycardi_num)}")
                        with col2 :
                            with st.expander("Médicament(s) bradycardisant(s)"):
                                for name in bradycardi_name : 
                                    st.write(f"\n {name}")
                    if np.sum(hypok_num) > 0 :
                          col1, col2 = st.columns(2)
                          col1.write(f"Nombre de médicament **hypokaliémiant** dans ce bilan médicamenteux : {np.sum(hypok_num)}")
                          with col2 :
                               with st.expander("Médicament(s) hypokaliémiant(s) du bilan médicamenteux"):
                                    for name in hypok_name : 
                                        st.write(f"\n {name}")

                if np.sum(hypok_num) > 0 or np.sum(hyperk_num) > 0 :
                    st.write(" ----------------------------- ") 
                    st.write("**Analyse du risque de dyskaliémie :**") 

                    if np.sum(hyperk_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **hyperkaliémiant** dans ce bilan médicamenteux : {np.sum(hyperk_num)}")
                        with col2 :
                            with st.expander("Médicament(s) hyperkaliémiant(s) du bilan médicamenteux"):
                                for name in hyperk_name : 
                                    st.write(f"\n {name}")                
                    if np.sum(hypok_num) > 0 :
                        col1, col2 = st.columns(2)
                        col1.write(f"Nombre de médicament **hypokaliémiant** dans ce bilan médicamenteux : {np.sum(hypok_num)}")
                        with col2 :
                            with st.expander("Médicament(s) hypokaliémiant(s) du bilan médicamenteux"):
                                for name in hypok_name : 
                                    st.write(f"\n {name}") 
                
                if np.sum(anticholinergics_num) > 0 :
                    st.write(" ----------------------------- ")
                    st.write("**Analyse du risque de syndrome anticholinergique :**") 
                    col1, col2 = st.columns(2)
                    col1.write(f"Nombre de médicament **anticholinergique** dans ce bilan médicamenteux : {np.sum(anticholinergics_num)}")
                    with col2 :
                        with st.expander("Médicament(s) anticholinergique(s) du bilan médicamenteux"):
                            for name in anticholinergics_name : 
                                st.write(f"\n {name}")
                
                if np.sum(pro_convuls_num) > 0 :
                    st.write(" ----------------------------- ")
                    st.write("**Analyse du risque de convulsion chez le patient épileptique :**") 
                    col1, col2 = st.columns(2)
                    col1.write(f"Nombre de médicament **proconvulsivant** dans ce bilan médicamenteux : {np.sum(pro_convuls_num)}")
                    with col2 :
                        with st.expander("Médicament(s) proconvulsivant(s) du bilan médicamenteux"):
                            for name in pro_convuls_name : 
                                st.write(f"\n {name}")
                                

            st.sidebar.write(" ----------------------------- ")    

            Listes_medocs = pd.read_csv('Listes_medicaments.csv')
            Listes_medocs.set_index('Index_L', inplace=True)

            option2 = st.sidebar.selectbox(
                 "Choisis une liste pour la consulter.",
                 Listes_medocs.index)

            if option2 != "# Choisir une liste de médicaments"  :
                 st.text_area(option2, 
                              f"{Listes_medocs.loc[{str(option2)}, 'Listes'][0]}",
                              key = option2)
        run()
# -----------------------------------------------------------------------------

def about():
    st.sidebar.markdown('---')
    st.sidebar.info('''
        Pour toutes suggestions d'ajout ou de modification, n'hésitez pas à conctacter le Dr. [Elsa Jouhanneau](mailto:ejouhanneau@ch-lemans.fr).
    ''')
    st.sidebar.write("Made by [Arthur Carré](mailto:arthur.carre@icloud.com) with **_Streamlit_**") 

# -----------------------------------------------------------------------------
     
if __name__ == "__main__":
    main()
    about()
