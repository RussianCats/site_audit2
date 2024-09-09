import os
import subprocess
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Путь для загрузки файлов
UPLOAD_FOLDER = r'C:\Users\pima\Documents\test\site_folder'
ALLOWED_EXTENSIONS = {'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Проверка допустимого расширения
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Главная страница с формой для загрузки файла
@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <title>Загрузка архива</title>
    <h1>Загрузите ZIP архив</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <input type="submit" value="Загрузить">
    </form>
    '''

# Обработка загрузки и распаковки архива
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Файл не был отправлен'
    
    file = request.files['file']

    if file.filename == '':
        return 'Файл не был выбран'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Сохраняем загруженный файл
        file.save(file_path)

        # Путь к системному архиватору (7-Zip, WinRAR и т.д.)
        # Убедитесь, что архиватор установлен и путь указан корректно.
        seven_zip_path = r'C:\Program Files\7-Zip\7z.exe'  # Укажите путь к 7z.exe

        # Команда для распаковки архива с помощью 7-Zip
        extract_command = [seven_zip_path, 'x', file_path, '-o' + app.config['UPLOAD_FOLDER'], '-y']

        try:
            # Выполняем команду через subprocess
            subprocess.run(extract_command, check=True)
        except subprocess.CalledProcessError as e:
            return f"Ошибка при распаковке архива: {str(e)}"

        # Удаляем загруженный ZIP файл после распаковки
        os.remove(file_path)

        return f'Архив {filename} успешно загружен и распакован с использованием 7-Zip!'
    else:
        return 'Недопустимый формат файла. Пожалуйста, загрузите ZIP архив.'

if __name__ == '__main__':
    app.run(debug=True)
