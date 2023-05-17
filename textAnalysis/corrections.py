import os
import re

directory = "/Users/mariemccormick/PycharmProjects/AciduleApp/transcriptions"

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as file:
            content = file.read()

        # Replace 'lozan' with 'lausanne' in the content
        content = re.sub(r"losanne|lozan", "lausanne", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneoise|lozanoise", "lausannoise", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneois|lozanois", "lausannois", content, flags=re.IGNORECASE)
        content = re.sub(r"asideul|sidule", "acidule", content, flags=re.IGNORECASE)
        content = re.sub(r"yagy", "jaggi", content, flags=re.IGNORECASE)
        content = re.sub(r"venage", "venoge", content, flags=re.IGNORECASE)

        #'aacidule',
        # chahy = chailly
        # l'Ousanne
        # gol = goal S00040_P169_Conseil_Communal_Lausanne_1990_11_0
        # enlever ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
        # dans les transcriptions
        with open(file_path, "w") as file:
            file.write(content)
