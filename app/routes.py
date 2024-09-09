from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from app.utils.file_utils import extract_zip_file

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Файл не был отправлен'
    
    file = request.files['file']
    if file.filename == '':
        return 'Файл не был выбран'
    
    if file and file.filename.endswith('.zip'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Сохраняем файл
        file.save(file_path)

        # Используем утилиту для распаковки
        error = extract_zip_file(file_path, app.config['UPLOAD_FOLDER'])
        if error:
            return f'Ошибка при распаковке: {error}'

        return f'Файл {filename} успешно загружен и распакован.'
    else:
        return 'Пожалуйста, загрузите ZIP файл.'
