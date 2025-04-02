import os

dir_path = os.path.dirname(os.path.abspath(__file__))
folder_path = dir_path.capitalize() + r"\battery-report"  # Change this path accordingly

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)

print("All files deleted successfully.")