import os
import subprocess
import time
import random

def extract_zip_file(zip_path, extract_to):
    seven_zip_path = r'C:\Program Files\7-Zip\7z.exe'  # Путь к 7-Zip
    extract_command = [seven_zip_path, 'x', zip_path, '-o' + extract_to, '-y']
    try:
        subprocess.run(extract_command, check=True)
    except subprocess.CalledProcessError as e:
        return str(e)
    os.remove(zip_path)

    return None

def generate_name_userspace():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])
 
    return f"space-{timestamp}-{random_numbers}"