import os
import re

directory = "../transcriptions"

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as file:
            content = file.read()

        content = re.sub(r"leuze\s|lozane\s|losanne\s|lozan\s|l'(O|o)usanne\s|losan\s|lausann\s|alausanne\s|losann\s", "lausanne", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneoise\s|lozanoise\s|Los Anoises|loisanoise\s|lozanoisse\s", "lausannoise", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneois\s|lozanois\s|lezanoi\s|losanoi\s|lezanois\s|loisanoi\s|loisanoin\s", "lausannois", content, flags=re.IGNORECASE)
        content = re.sub(r"asacidule\s|asideul\s|de sidule\s|assydul\s|sidule\s|aacidule\s|la sidule\s", "acidule", content, flags=re.IGNORECASE)
        content = re.sub(r"yagy|Yagui", "jaggi", content, flags=re.IGNORECASE)
        content = re.sub(r"venage", "venoge", content, flags=re.IGNORECASE)
        content = re.sub(r"gol", "goal", content, flags=re.IGNORECASE)
        content = re.sub(r"vvf", "wwf", content, flags=re.IGNORECASE)
        content = re.sub(r"jeunvoi", "genevois", content, flags=re.IGNORECASE)
        content = re.sub(r"chahy", "chailly", content, flags=re.IGNORECASE)
        content = re.sub(r"dolce viter|Delcevita", "Dolce Vita", content, flags=re.IGNORECASE)
        content = re.sub(r"Téchard", "Richard", content, flags=re.IGNORECASE)
        content = re.sub(r"orpiste", "hors-piste", content, flags=re.IGNORECASE)
        content = re.sub(r"sougar", "sous-gare", content, flags=re.IGNORECASE)
        content = re.sub(r"en Seuleillé", "ensoleillé", content, flags=re.IGNORECASE)
        content = re.sub(r"jandaniell", "Jean-Daniel", content, flags=re.IGNORECASE)

        with open(file_path, "w") as file:
            file.write(content)
