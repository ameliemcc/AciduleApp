# AciduleApp
## Cours UNIL : Projet de développement logiciel
Professeur : Davide Picca \
Etudiante : Amélie McCormick

## Introduction
Radio Acidule was a local station that covered news from Lausanne & beyond, from 1984 to 1999. This Web App suggests a new way to explore the Acidule corpus.  
Some recordings are available online on the Web TV run by the Archives of Lausanne : https://www.dartfish.tv/Videos?CR=p33203c501361#AQEBAAEEAXGmBwAAAQEHAAABAgEBBgdhY2lkdWxlAQAAAAAA 
## Usage instructions
Make sure the necessary packages are installed by running:
```
 pip install -r requirements.txt
```

Start the Streamlit app by running:
```
streamlit run Recherche_par_mot.py
```
## Functionalities
The app presents two main pages. 
*Recherche par mot* : Allows the user to write a word they wish to look for in the transcriptions, or to select one from a scrollable list. 
The user can also pick a title of an *émission* to have its transcription displayed. \
*Recherche par topic* : This page might take some time to load, as it displays the LDA Intertopic Distance Map, which presents the topics that come up in the corpus. 
Under the graph, the user can see which *émissions* are most linked to which topic. 

## Project structure
The repository also contains the code used to format the data and add it to the database. The two pages that make the app are *Recherche_par_topic.py* and *Recherche_par_mot.py*.

