import os
import subprocess
from flask import render_template, request, session, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from app.utils.file_utils import extract_zip_file, generate_name_userspace

# Установите секретный ключ для сессий
app.secret_key = 'ds=-docODWDo;=-ewqdkw0=1e3'

@app.route('/')
def index():
    # Проверяем, существует ли уже userspace в сессии, если нет - генерируем
    userspace = session['userspace']
    return render_template('index.html', userspace=userspace)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Используем userspace из сессии
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
            command = [r'D:\main\develop\audit2\venv\Scripts\taudit2.exe', '--pathd', pathd]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Дождаться завершения процесса
            process.wait()

            # Найдем лог-файл в папке userspace
            log_file = None
            for f in os.listdir(pathd):
                if f.endswith('.log'):
                    log_file = f
                    break

            # Считаем содержимое лог-файла
            log_content = ''
            if log_file:
                log_file_path = os.path.join(pathd, log_file)
                with open(log_file_path, 'r', encoding='cp1251') as f:
                    log_content = f.read()

            # Получим список файлов из папки report
            report_folder = os.path.join(pathd, 'report')
            report_files = []
            if os.path.exists(report_folder):
                report_files = os.listdir(report_folder)

            # Отправляем пользователя на страницу с результатами
            return render_template('result.html', userspace=userspace, log_content=log_content, files=report_files)

        except Exception as e:
            return f'Ошибка при запуске taudit2: {str(e)}'
    else:
        return 'Пожалуйста, загрузите ZIP файл.'


# Маршрут для скачивания файлов из папки report
@app.route('/download/<filename>')
def download_file(filename):
    if 'userspace' in session:
        userspace = session['userspace']
        report_folder = os.path.join(app.config['UPLOAD_FOLDER'], userspace, 'report')
        return send_from_directory(report_folder, filename)
    return 'Файл не найден'
