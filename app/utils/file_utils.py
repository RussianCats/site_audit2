import os
import subprocess

def extract_zip_file(zip_path, extract_to):
    seven_zip_path = r'C:\Program Files\7-Zip\7z.exe'  # Путь к 7-Zip
    extract_command = [seven_zip_path, 'x', zip_path, '-o' + extract_to, '-y']

    try:
        subprocess.run(extract_command, check=True)
    except subprocess.CalledProcessError as e:
        return str(e)

    # Удаление архива после распаковки
    os.remove(zip_path)
    return None
