import shutil
import sys
import os
import re
import zipfile

from pathlib import Path


def sorting_files(path):
    # Список назв папок, які ми створюємо
    folders = ['images', 'documents', 'audio', 'video', 'archives', 'unknown_extensions']
    # Цикл для створення кожної папки
    for folder in folders:
        (path / folder).mkdir(exist_ok=True)
    print("Директорії створено")
    
    # Знаходимо файли з вказаними розширеннями у всіх вкладених папках (документи)
    documents_extensions = ['.doc', '.docs', '.txt', '.pdf', '.xlsx', '.pptx']
    for ext in documents_extensions:
        for doc in path.glob(f'**/*{ext}'):
            # Перевірка чи doc є файлом
            if doc.is_file():
                # Отримуємо тільки ім'я файлу без шляху
                f_name = doc.name
                normalized_file = normalize(f_name)
                # Використовуємо shutil.move для переміщення файлу до нової папки
                new_path = path.joinpath('documents', normalized_file)
                shutil.move(str(doc), str(new_path))
    print("Відсортовано документи")
    
    # Знаходимо файли з вказаними розширеннями у всіх вкладених папках (зображення)
    images_extensions = ['.jpeg', '.png', '.jpg', '.svg']
    for ext in images_extensions:
        for doc in path.glob(f'**/*{ext}'):
            # Перевірка чи doc є файлом
            if doc.is_file():
                # Отримуємо тільки ім'я файлу без шляху
                f_name = doc.name
                normalized_file = normalize(f_name)
                # Використовуємо shutil.move для переміщення файлу до нової папки
                new_path = path.joinpath('images', normalized_file)
                shutil.move(str(doc), str(new_path))
    print("Відсортовано зображення")
    
    # Знаходимо файли з вказаними розширеннями у всіх вкладених папках (музика)
    audio_extensions = ['.mp3', '.ogg', '.wav', '.amr']
    for ext in audio_extensions:
        for doc in path.glob(f'**/*{ext}'):
            # Перевірка чи doc є файлом
            if doc.is_file():
                # Отримуємо тільки ім'я файлу без шляху
                f_name = doc.name
                normalized_file = normalize(f_name)
                # Використовуємо shutil.move для переміщення файлу до нової папки
                new_path = path.joinpath('audio', normalized_file)
                shutil.move(str(doc), str(new_path))
    print("Відсортовано музику")
    
    # Знаходимо файли з вказаними розширеннями у всіх вкладених папках (відео)
    video_extensions = ['.avi', '.mp4', '.mov', '.mkv']
    for ext in video_extensions:
        for doc in path.glob(f'**/*{ext}'):
            # Перевірка чи doc є файлом
            if doc.is_file():
                # Отримуємо тільки ім'я файлу без шляху
                f_name = doc.name
                normalized_file = normalize(f_name)
                # Використовуємо shutil.move для переміщення файлу до нової папки
                new_path = path.joinpath('video', normalized_file)
                shutil.move(str(doc), str(new_path))
    print("Відсортовано відео")

# Знаходимо архіви з вказаними розширеннями у всіх вкладених папках
    archives_extensions = ['.zip', '.gz', '.tar', '.ZIP', '.GZ', '.TAR']
    for ext in archives_extensions:
        for arh in path.glob(f'**/*{ext}'):
            # Перевірка чи arh є файлом
            if arh.is_file():
                try:
                    with zipfile.ZipFile(arh, 'r') as zip_ref:
                        # Отримуємо ім'я архіву
                        arh_full_name = arh.name
                        arh_name, arh_extension = os.path.splitext(arh_full_name)
                        new_arh = path.joinpath('archives', arh_name)
                        shutil.unpack_archive(arh, new_arh)
                        os.remove(arh)                       
                except zipfile.BadZipFile:
                    print(f"Помилка: {arh.name} — архів пошкоджений")
                    os.remove(arh)
                    continue
                except zipfile.LargeZipFile:
                    print(f"Помилка: {arh.name} — архів занадто великий")
                    os.remove(arh)
                    continue
                except Exception as e:
                    print(f"Помилка при роботі з {arh.name}: {e}")
                    os.remove(arh)
                    continue
    print("Архіви оброблено")

    # Переміщуємо файли, що залишилися
    # Шукаємо по директоріях
    for doc in path.glob('*/'):
        folder_name = doc.name
        if folder_name not in folders:
            new_folder_name = Path(str(path),folder_name)
            for doc_unk in new_folder_name.glob('**/*'):
                    # для файлів - перейменування і перенесення
                if doc_unk.is_file():
                        # Отримуємо тільки ім'я файлу без шляху
                    f_name = doc_unk.name
                    normalized_file = normalize(f_name)
                        # Використовуємо shutil.move для переміщення файлу до нової папки
                    new_path = path.joinpath('unknown_extensions', normalized_file)
                    shutil.move(str(doc_unk), str(new_path))
                else:
                    continue
        else:
            continue
                # Видаляємо пусті папки
        for dir_empt in path.glob('**/*'):
            if dir_empt.is_dir() and not dir_empt.stem in folders and not any(dir_empt.glob('*')):  #.stem - бере назву папки у в тебе був повністю весь шлях
                try:                        #### vykluchaemo pomylky
                    dir_empt.rmdir()
                except FileExistsError:
                    pass


def normalize(f_name):
    # робимо словник для транслітерації
    symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЄІЇҐ"
    translit = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "A", "B", "V", "G", "D", "E", "E", "J", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
               "F", "H", "TS", "CH", "SH", "SCH", "", "Y", "", "E", "YU", "YA", "JE", "I", "JI", "G")
    trans = {}
    for s, t in zip(symbols, translit):
        trans[ord(s)] = t
        # Відокремлюємо ім'я файлу та розширення
    file_name, file_extension = os.path.splitext(f_name)
        # перекладаємо ім'я файла
    normalized_name = file_name.translate(trans)
        # замінюємо спеціальні символи
    normalized_file_name = re.sub(r'\W', '_', normalized_name)
        # З'єднуємо нормалізоване ім'я з розширенням
    normalized_file = f"{normalized_file_name}{file_extension}"
    return normalized_file


def main():
    args = sys.argv
    args_string = ' '.join(args)
    print(args_string)
# Перевіряємо кількість аргументів
    if len(sys.argv) != 2:
        print('Incorrect data')
        sys.exit(1)
# Перевіряємо, чи є другий аргумент папкою
    else:
        user_input = sys.argv[1]
        path = Path(user_input)
    # Якщо всі перевірки пройшли, то запускаємо основну функцію item
        if path.exists():
            if path.is_dir():
                sorting_files(path)
        else:
            print(f'{path.absolute} is not exists')
    

if __name__ == '__main__':
    main()