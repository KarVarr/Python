# file_handler.py
import os
import json
from pathlib import Path
from config import CONFIG_FILE

def validate_file_path(file_path):
    """Проверяет и нормализует пути к файлам"""
    if not file_path.startswith('/'):
        file_path = '/' + file_path
    
    path = Path(file_path).resolve()
    
    if not path.parent.exists():
        raise ValueError(f"Директория не существует: {path.parent}")
    
    return str(path)

def get_valid_file_paths():
    """Запрашивает у пользователя пути к файлам с валидацией"""
    while True:
        try:
            input_path = input("Введите путь к входному файлу Excel: ")
            input_path = validate_file_path(input_path)
            
            if not os.path.isfile(input_path):
                print(f"Файл не найден: {input_path}")
                continue
                
            output_path = input("Введите путь для сохранения результатов (включая имя файла.xlsx): ")
            output_path = validate_file_path(output_path)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            return input_path, output_path
            
        except ValueError as e:
            print(f"Ошибка: {str(e)}")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            print("Пожалуйста, попробуйте снова.")

def load_training_files():
    """Загружает список файлов для обучения"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('training_files', [])
    return []

def save_training_files(files):
    """Сохраняет список файлов для обучения"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'training_files': files}, f)