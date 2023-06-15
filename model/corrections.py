import os
import re

DIRECTORY = "../transcriptions"

for filename in os.listdir(DIRECTORY):
    if filename.endswith(".txt"):
        file_path = os.path.join(DIRECTORY, filename)
        with open(file_path, "r") as file:
            content = file.read()

        content = re.sub(r"leuze\s|lozane\s|losanne\s|lozan\s|l'(O|o)usanne\s|"
                         r"losan\s|lausann\s|alausanne\s|losann\s|leusanne\s",
                         "lausanne ", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneoise\s|lozanoise\s|Los Anoises|loisanoise\s|"
                         r"lozanoisse\s", "lausannoise ", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneois\s|lozanois\s|lezanoi\s|losanoi\s|lezanois\s|"
                         r"loisanoi\s|loisanoin\s|nozanois", "lausannois ", content,
                         flags=re.IGNORECASE)
        content = re.sub(r"asacidule\s|asideul\s|de sidule\s|Asidule\s|assydul\s|sidule\s|"
                         r"aacidule\s|la sidule\s", "acidule ", content, flags=re.IGNORECASE)
        content = re.sub(r"Ivétiagi", "Yvette Jaggi ", content, flags=re.IGNORECASE)
        content = re.sub(r"Palue", "Palud", content, flags=re.IGNORECASE)

        content = re.sub(r"yagy|Yagui", "jaggi ", content, flags=re.IGNORECASE)
        content = re.sub(r"venage", "venoge ", content, flags=re.IGNORECASE)
        content = re.sub(r"gol", "goal ", content, flags=re.IGNORECASE)
        content = re.sub(r"vvf", "wwf ", content, flags=re.IGNORECASE)
        content = re.sub(r"jeunvoi", "genevois ", content, flags=re.IGNORECASE)
        content = re.sub(r"chahy", "chailly ", content, flags=re.IGNORECASE)
        content = re.sub(r"dolce viter|Delcevita", "Dolce Vita ", content, flags=re.IGNORECASE)
        content = re.sub(r"Téchard", "Richard ", content, flags=re.IGNORECASE)
        content = re.sub(r"orpiste", "hors-piste ", content, flags=re.IGNORECASE)
        content = re.sub(r"sougar", "sous-gare ", content, flags=re.IGNORECASE)
        content = re.sub(r"en Seuleillé", "ensoleillé ", content, flags=re.IGNORECASE)
        content = re.sub(r"jandaniell", "Jean-Daniel ", content, flags=re.IGNORECASE)
        content = re.sub(r"aiti", "Haïti ", content, flags=re.IGNORECASE)
        content = re.sub(r"écosser", "écossais ", content, flags=re.IGNORECASE)
        content = re.sub(r"écoce", "Écosse ", content, flags=re.IGNORECASE)
        content = re.sub(r"cronique", "chronique ", content, flags=re.IGNORECASE)
        content = re.sub(r"buhaj", "Buache ", content, flags=re.IGNORECASE)





        # noyenne = doyenne
        with open(file_path, "w") as file:
            file.write(content)
