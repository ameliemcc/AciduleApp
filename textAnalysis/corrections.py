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
        content = re.sub(r"lausanneoise", "lausannoise", content, flags=re.IGNORECASE)
        content = re.sub(r"lausanneois", "lausannois", content, flags=re.IGNORECASE)
        #   'asideul',
        #   'sidule',
        #   'yagy',
        with open(file_path, "w") as file:
            file.write(content)