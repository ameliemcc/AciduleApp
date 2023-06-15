import os
import shutil
music_folder = '/Users/mariemccormick/PycharmProjects/AciduleApp/docs/music'
source_folder = '/Users/mariemccormick/PycharmProjects/AciduleApp/docs/keep'  # Replace with the path to your source folder
delete_folder = '/Users/mariemccormick/PycharmProjects/AciduleApp/docs/delete'  # Replace with the path to your keep folder
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)

    # Iterate over each file in the delete folder
for filename in os.listdir(music_folder):
    file_path = os.path.join(music_folder, filename)

    # Check if the path corresponds to a file
    if os.path.isfile(file_path):
        print(filename)