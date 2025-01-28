# main.py
import pandas as pd
import os
from clothing_analyzer import ClothingAnalyzer
from file_handler import get_valid_file_paths, load_training_files, save_training_files

def process_file(input_path, output_path, training_files=None):
    """
    Обрабатывает файл и сохраняет результаты анализа
    """
    print("\nИнициализация анализатора...")
    analyzer = ClothingAnalyzer()
    
    if training_files:
        analyzer.train_on_existing_data(training_files)
    
    print("\nЧтение входного файла...")
    try:
        df = pd.read_excel(input_path)
        print(f"Загружено {len(df)} товаров для анализа")
    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
        return None
    
    print("\nНачало анализа товаров...")
    results = []
    error_rows = []
    
    for idx, row in df.iterrows():
        if idx % 10 == 0:
            print(f"Обработано {idx} товаров из {len(df)}")
        try:
            result = analyzer.analyze_item(row)
            if result is None:
                result = {
                    'Decision': 'NO',
                    'Score': 0.0,
                    'Reasons': f"Ошибка анализа товара (строка {idx + 1})"
                }
                error_rows.append(idx + 1)
            results.append(result)
        except Exception as e:
            print(f"Ошибка при анализе строки {idx + 1}: {str(e)}")
            results.append({
                'Decision': 'NO',
                'Score': 0.0,
                'Reasons': f"Ошибка обработки: {str(e)}"
            })
            error_rows.append(idx + 1)
    
    # Добавляем результаты анализа в DataFrame
    df['Decision'] = [r['Decision'] for r in results]
    df['Score'] = [r['Score'] for r in results]
    df['Reasons'] = [r['Reasons'] for r in results]
    
    # Подсчет статистики
    yes_count = sum(1 for r in results if r['Decision'] == 'YES')
    print(f"\nРезультаты анализа:")
    print(f"Всего товаров: {len(df)}")
    print(f"Рекомендовано к покупке (YES): {yes_count}")
    print(f"Не рекомендовано (NO): {len(df) - yes_count}")
    
    if error_rows:
        print("\nВнимание! Были ошибки при анализе следующих строк:")
        print(", ".join(map(str, error_rows)))
    
    # Сохранение результатов
    try:
        print("\nСохранение результатов...")
        df.to_excel(output_path, index=False)
        print(f"Результаты успешно сохранены в {output_path}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {str(e)}")
        return None
    
    return df

def main():
    """
    Основная функция программы
    """
    print("=" * 50)
    print("Программа анализа товаров")
    print("=" * 50)
    
    try:
        # Получение путей к файлам
        input_file, output_file = get_valid_file_paths()
        
        # Загрузка файлов для обучения
        training_files = load_training_files()
        if not training_files:
            print("\nФайлы для обучения не найдены.")
            training_files_input = input("Введите пути к файлам для обучения через запятую (или Enter для пропуска): ")
            if training_files_input:
                training_files = []
                for file_path in [f.strip() for f in training_files_input.split(',')]:
                    try:
                        if os.path.isfile(file_path):
                            training_files.append(file_path)
                        else:
                            print(f"Предупреждение: Файл не найден: {file_path}")
                    except Exception as e:
                        print(f"Предупреждение: Неверный путь к файлу {file_path}: {str(e)}")
                
                if training_files:
                    save_training_files(training_files)
        
        # Обработка файла
        results_df = process_file(input_file, output_file, training_files)
        
        if results_df is not None:
            print("\nАнализ успешно завершен!")
        else:
            print("\nПроизошла ошибка при обработке файла.")
            
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла неожиданная ошибка: {str(e)}")
    finally:
        print("\nЗавершение работы программы.")
        print("=" * 50)

if __name__ == "__main__":
    main()