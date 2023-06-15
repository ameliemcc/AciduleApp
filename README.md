# AciduleApp
## Projet de développement logiciel
En collaboration avec les Archives de la Ville de Lausanne \
Professeur : Davide Picca \
Etudiante : Amélie McCormick 

### Introduction
La station lausannoise Radio Acidule a diffusé des émissions touchant des thèmes variés entre 1984 et 1999. Des 
reportages sur la gestion des eaux usées, aux retranscriptions en direct des séances du conseil communal, en passant par
des émissions destinées spécifiquement au retraités, les ondes d'Acidule ont porté des voix très diverses. 

### But du projet
- Transcription des émissions du corpus Acidule
- Analyse textuelle ayant pour but de déduire les thèmes abordés dans les émissions
- Développement d'une web app permettant l'accès aux archives

Cette App permet d'explorer le corpus Acidule 
Les enregistrements sont disponibles en ligne sur la Web TV des Archives de Lausanne: https://www.dartfish.tv/Videos?CR=p33203c501361#AQEBAAEEAXGmBwAAAQEHAAABAgEBBgdhY2lkdWxlAQAAAAAA

## Utilisation
### Mise en place
Assurez-vous d'avoir installé les packages nécessaires en exécutant :
```
 pip install -r requirements.txt
```

Démarrez l'application en exécutant :
```
streamlit run Recherche_par_mot.py
```
### Fonctionnalités
L'application présente deux pages principales.\
*Recherche par mot* : Permet à l'utilisateur d'écrire un mot qu'il souhaite rechercher dans les transcriptions, ou de le sélectionner dans une liste déroulante.
L'utilisateur peut également choisir le titre d'une émission pour afficher sa transcription.
*Recherche par topic* : Cette page affiche la carte de distance intertopic LDA, qui offre une représentation visuelle des thèmes qui apparaissent dans le corpus.
Sous le graphique, l'utilisateur peut voir quelles émissions sont le plus liées à quel sujet.


### Structure du projet
Le code ayant été utilisé pour créer la base de donnée et entrainer le modèle d'analyse textuelle est contenu dans le fichier *model* Les documents *Recherche_par_topic.py* et *Recherche_par_mot.py* sont à l'origine des deux pages principales de l'app. 

