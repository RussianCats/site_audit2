
import os
import subprocess
from app import app
from werkzeug.utils import secure_filename
from flask import render_template, request, session
from app.utils.file_utils import extract_zip_file, generate_name_userspace

# Установите секретный ключ для сессий
app.secret_key = 'ds=-docODWDo;=-ewqdkw0=1e3'

@app.route('/')
def index():
    # Проверяем, существует ли уже userspace в сессии, если нет - генерируем
    if 'userspace' not in session:
        session['userspace'] = generate_name_userspace()
    
    # Теперь userspace доступен через сессию
    userspace = session['userspace']
    return render_template('index.html', userspace=userspace)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Используем userspace из сессии
    if 'userspace' not in session:
        session['userspace'] = generate_name_userspace()
    
    userspace = session['userspace']

    if 'file' not in request.files:
        return 'Файл не был отправлен'
    
    file = request.files['file']
    if file.filename == '':
        return 'Файл не был выбран'
    
    if file and file.filename.endswith('.zip'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], userspace, "database")
        file_path_name = os.path.join(app.config['UPLOAD_FOLDER'], userspace, filename)

        # Создаем папку, если она не существует
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Сохраняем файл
        file.save(file_path_name)

        # Используем утилиту для распаковки
        error = extract_zip_file(file_path_name, file_path)
        if error:
            return f'Ошибка при распаковке: {error}'

        # Путь, который будет передан в качестве аргумента
        pathd = os.path.join(app.config['UPLOAD_FOLDER'], userspace)

        # Запуск внешнего скрипта taudit2.exe в отдельном процессе
        try:
            # Формируем команду для запуска
            command = [r'D:\main\develop\audit2\venv\Scripts\taudit2.exe', '--pathd', pathd]

            # Запускаем процесс асинхронно
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Возвращаем пользователю сообщение об успешной загрузке и распаковке,
            # а процесс taudit2 будет выполнен асинхронно
            return f'Файл {filename} успешно загружен, распакован и обработка началась.'

        except Exception as e:
            return f'Ошибка при запуске taudit2: {str(e)}'
    else:
        return 'Пожалуйста, загрузите ZIP файл.'