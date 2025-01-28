import pandas as pd
import numpy as np
from PIL import Image
import requests
import json
import os
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

CONFIG_FILE = 'ml_config.json'

class ClothingAnalyzer:
    def __init__(self):
        self.image_model = ResNet50(weights='imagenet')
        
        self.fragile_categories = [
            'Glass', 'Vase', 'Cup', 'Glass set', 'Plate set',
            'Bowl', 'Wine glass', 'Drinking glass', 'Ceramic'
        ]
        
        self.reject_sizes = {
            'general': ['XXS', 'XS'],
            'women_bottoms': ['32', '34'],
            'men': ['XS'],
            'women_shoes': ['35', '42'],
            'men_shoes': [str(i) for i in range(35, 41)]
        }
        
        self.allowed_small_bra = ['70A', '75A']
        
        self.bad_bra_sizes = [
            '70E', '70F', '75E', '75F',
            '80A', '80E', '80F', '85A', '85E', '85F',
            '90A', '90E', '90F', '95A', '95E', '95F'
        ]

        self.basic_colors = [
            'Black', 'White', 'Grey', 'Navy', 'Beige', 'Dark blue',
            'Light grey', 'Dark grey', 'Cream', 'Light beige', 'Off-white'
        ]
        
        self.basic_categories = [
            'T-shirt', 'Top', 'Socks', 'Leggings', 'Underwear', 'Bra',
            'Briefs', 'Knickers', 'Tank top', 'Basic T-shirt', 'Basic top'
        ]
        
        self.exclude_categories = [
            'Make-up bag', 'Cosmetic bag', 'Wash bag', 'Beauty box',
            'Eyebrow pencil', 'Lipstick', 'Mascara', 'Foundation',
            'Concealer', 'Powder', 'Blush', 'Eyeshadow'
        ]
        
        self.winter_categories = [
            'Jacket', 'Coat', 'Winter boots', 'Sweater', 'Cardigan',
            'Scarf', 'Gloves', 'Hat', 'Winter accessories'
        ]
        
        self.multi_item_categories = ['Set', 'Pack', 'Kit', 'Bundle']
        self.curtain_min_size = 120

    def train_on_existing_data(self, training_files):
        print("\nНачало обучения на существующих данных:")
        total_yes = 0
        total_files = 0
        
        for file in training_files:
            try:
                print(f"\nОбработка файла: {file}")
                df = pd.read_excel(file)
                if 'Decision' in df.columns:
                    positive_examples = df[df['Decision'] == 'YES']
                    total_yes += len(positive_examples)
                    
                    if 'Category' in positive_examples:
                        new_categories = positive_examples['Category'].dropna().unique()
                        orig_cat_count = len(self.basic_categories)
                        self.basic_categories.extend(new_categories)
                        self.basic_categories = list(set(self.basic_categories))
                        print(f"Добавлено новых категорий: {len(self.basic_categories) - orig_cat_count}")
                        print("Новые категории:", [cat for cat in new_categories if cat not in self.basic_categories[:orig_cat_count]])
                        
                    if 'Color' in positive_examples:
                        new_colors = positive_examples['Color'].dropna().unique()
                        orig_color_count = len(self.basic_colors)
                        self.basic_colors.extend(new_colors)
                        self.basic_colors = list(set(self.basic_colors))
                        print(f"Добавлено новых цветов: {len(self.basic_colors) - orig_color_count}")
                        print("Новые цвета:", [color for color in new_colors if color not in self.basic_colors[:orig_color_count]])
                    
                    total_files += 1
                    print(f"Успешных товаров в файле: {len(positive_examples)}")
                    
            except Exception as e:
                print(f"Ошибка при обработке файла {file}: {str(e)}")
                continue
        
        print(f"\nИтоги обучения:")
        print(f"Обработано файлов: {total_files}")
        print(f"Всего успешных товаров: {total_yes}")
        print(f"Итоговое количество базовых категорий: {len(self.basic_categories)}")
        print(f"Итоговое количество базовых цветов: {len(self.basic_colors)}")

    def analyze_image(self, url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            predictions = self.image_model.predict(img_array)
            decoded = decode_predictions(predictions, top=5)[0]
            
            is_basic = any(tag in [d[1] for d in decoded] 
                         for tag in ['t_shirt', 'jersey', 'sock', 'leggings'])
            is_kids = any(tag in [d[1] for d in decoded]
                        for tag in ['toy', 'pajama', 'school_uniform'])
            is_multi_item = any(tag in [d[1] for d in decoded] 
                             for tag in ['suit', 'pair', 'set', 'collection'])
            is_fancy_dress = any(tag in [d[1] for d in decoded]
                              for tag in ['miniskirt', 'cocktail_dress', 'ballgown'])
            is_crop_top = any(tag in [d[1] for d in decoded]
                           for tag in ['brassiere', 'bandeau'])
            
            return {
                'basic': is_basic,
                'kids': is_kids,
                'multi_item': is_multi_item,
                'item_count': 2 if is_multi_item else 1,
                'fancy_dress': is_fancy_dress,
                'crop_top': is_crop_top
            }
        except:
            return {
                'basic': False,
                'kids': False,
                'multi_item': False,
                'item_count': 1,
                'fancy_dress': False,
                'crop_top': False
            }

    def check_size(self, size, category, gender):
        if pd.isna(size) or pd.isna(category):
            return False, "Отсутствуют данные о размере или категории"
            
        size_str = str(size).upper()
        
        if 'KIDS' not in str(gender).upper():
            if any(reject in size_str for reject in self.reject_sizes['general']):
                return False, f"Размер {size_str} - низкий спрос"

        if str(gender).upper() == 'WOMEN':
            if category in ['Trousers', 'Jeans', 'Leggings', 'Shorts']:
                if size_str in self.reject_sizes['women_bottoms']:
                    return False, f"Маленький размер для женской одежды ({size_str})"
            if category == 'Shoes':
                if size_str in self.reject_sizes['women_shoes']:
                    return False, f"Нестандартный размер женской обуви ({size_str})"

        if str(gender).upper() == 'MEN':
            if size_str in self.reject_sizes['men']:
                return False, f"Размер {size_str} для мужской одежды - низкий спрос"
            if category == 'Shoes':
                if size_str in self.reject_sizes['men_shoes']:
                    return False, f"Маленький размер мужской обуви ({size_str})"
        
        if category == 'Bra':
            if size_str in self.bad_bra_sizes and size_str not in self.allowed_small_bra:
                return False, f"Непопулярный размер бюстгальтера ({size_str})"
        
        if 'curtain' in str(category).lower():
            try:
                curtain_size = float(str(size).split('x')[0])
                if curtain_size >= self.curtain_min_size:
                    return True, f"Шторы подходящего размера ({curtain_size}см)"
            except:
                pass
                
        return True, "Стандартный размер"

    def analyze_item(self, row):
        score = 0
        positive_reasons = []
        negative_reasons = []

        # Проверка размеров XS/XXS - немедленный отказ
        if pd.notna(row.get('Size')):
            size_str = str(row['Size']).upper()
            if 'XS' in size_str or 'XXS' in size_str:
                return {
                    'Decision': 'NO',
                    'Score': 0.0,
                    'Reasons': f"Отклонено: размер {size_str} не подходит для продажи"
                }
        
        # Проверка хрупких товаров
        if pd.notna(row.get('Category')) and any(frag in str(row['Category']) 
            for frag in self.fragile_categories):
            return {
                'Decision': 'NO',
                'Score': 0.0,
                'Reasons': f"Отклонено: хрупкий товар {row['Category']}"
            }
        
        # Проверка исключенных категорий
        if pd.notna(row.get('Category')) and row['Category'] in self.exclude_categories:
            return {
                'Decision': 'NO',
                'Score': 0.0,
                'Reasons': f"Отклонено: категория {row['Category']} исключена из рассмотрения"
            }
            
            # Анализ изображения если есть
        image_analysis = {
            'basic': False,
            'kids': False,
            'multi_item': False,
            'item_count': 1,
            'fancy_dress': False,
            'crop_top': False
        }
        if pd.notna(row.get('Photo link Parsing')):
            image_analysis = self.analyze_image(row['Photo link Parsing'])

        # Проверка платьев
        if row.get('Category') == 'Dress' and pd.notna(row.get('Photo link Parsing')):
            image_analysis = self.analyze_image(row['Photo link Parsing'])
            if image_analysis['fancy_dress']:
                return {
                    'Decision': 'NO',
                    'Score': 0.0,
                    'Reasons': "Неподходящий стиль платья (не базовая модель)"
                }

        # Проверка топов
        if row.get('Category') == 'Top' and pd.notna(row.get('Photo link Parsing')):
            image_analysis = self.analyze_image(row['Photo link Parsing'])
            if image_analysis['crop_top']:
                return {
                    'Decision': 'NO',
                    'Score': 0.0,
                    'Reasons': "Короткий топ - низкий спрос"
                }

        # Проверка маржи
        if pd.notna(row.get('RRP')) and pd.notna(row.get('sebes')):
            try:
                rrp = float(row['RRP'])
                cost = float(row['sebes'])
                
                rrp_rub = rrp * 105  # RRP в рублях
                cost_rub = cost  # Себестоимость из столбца sebes
                
                margin_percent = ((rrp_rub - cost_rub) / cost_rub) * 100
                
                if cost_rub > 700:  # Если себестоимость больше 700 рублей
                    if rrp_rub <= cost_rub:
                        score -= 0.2
                        negative_reasons.append(
                            f'Невыгодно: себестоимость {cost_rub:.0f}₽ больше или равна RRP {rrp_rub:.0f}₽ (маржа {margin_percent:.0f}%)'
                        )
                    elif rrp_rub > cost_rub * 1.3:  # Маржа минимум 30%
                        score += 0.2
                        positive_reasons.append(
                            f'Хорошая маржа {margin_percent:.0f}%: RRP {rrp_rub:.0f}₽ > себестоимость {cost_rub:.0f}₽'
                        )
                    else:
                        negative_reasons.append(
                            f'Низкая маржа {margin_percent:.0f}%: RRP {rrp_rub:.0f}₽ недостаточно выше себестоимости {cost_rub:.0f}₽'
                        )
            except Exception as e:
                print(f"Ошибка расчета маржи для артикула {row.get('Article ID')}: {str(e)}")
                print(f"RRP: {row.get('RRP')}, Cost: {row.get('sebes')}")
                negative_reasons.append('Ошибка расчета маржи')

        
        # Проверка размера
        size_ok, size_reason = self.check_size(
            row.get('Size'), 
            row.get('Category'), 
            row.get('Gender')
        )
        if not size_ok:
            negative_reasons.append(size_reason)
        else:
            score += 0.2
            positive_reasons.append(size_reason)
        
        # Проверка количества
        is_winter_item = row.get('Category') in self.winter_categories
        qty = float(row['QTY']) if pd.notna(row.get('QTY')) else 0
        
        if qty > 2 or (is_winter_item and qty >= 1):
            score += 0.3
            reason = 'Достаточное количество' if not is_winter_item else 'Зимняя одежда'
            positive_reasons.append(f'{reason}: {qty} шт.')
        else:
            negative_reasons.append(f'Недостаточное количество: {qty} шт.')
        
        is_multi_item = False
        if pd.notna(row.get('Description')):
            is_multi_item = any(word in str(row['Description']).lower() 
                             for word in self.multi_item_categories)
        item_multiplier = 2 if is_multi_item else 1
        
        if is_multi_item:
            score += 0.2
            positive_reasons.append('Набор предметов')
        
        if pd.notna(row.get('Photo link Parsing')):
            image_analysis = self.analyze_image(row['Photo link Parsing'])
            if image_analysis['multi_item']:
                item_multiplier = max(item_multiplier, image_analysis['item_count'])
                positive_reasons.append(f'Набор из {item_multiplier} предметов (анализ фото)')
            if image_analysis['basic']:
                score += 0.1
                positive_reasons.append('Базовая модель (анализ фото)')
            if image_analysis['kids']:
                score += 0.1
                positive_reasons.append('Детский товар (подтверждено фото)')
        
        if pd.notna(row.get('х2')):
            x2 = float(row['х2']) * item_multiplier
            if x2 > 2:
                score += 0.2
                positive_reasons.append(f'Хороший x2: {x2:.2f} (с учетом количества предметов)')
            else:
                negative_reasons.append(f'Низкий x2: {x2:.2f}')
        
        if pd.notna(row.get('Color')) and any(color.lower() in str(row['Color']).lower() 
                                             for color in self.basic_colors):
            score += 0.1
            positive_reasons.append(f'Базовый цвет: {row["Color"]}')
        else:
            negative_reasons.append(f'Небазовый цвет: {row.get("Color", "Нет данных")}')
            
        if pd.notna(row.get('Category')) and row['Category'] in self.basic_categories:
            score += 0.1
            positive_reasons.append(f'Базовая категория: {row["Category"]}')
        
        if pd.notna(row.get('Description')) and 'cashmere' in str(row['Description']).lower():
            score += 0.15
            positive_reasons.append('Кашемир')
        
        is_kids = False
        if pd.notna(row.get('Description')):
            is_kids = 'kids' in str(row['Description']).lower() or 'children' in str(row['Description']).lower()
        
        if is_kids:
            score += 0.1
            positive_reasons.append('Детский товар')
            if pd.notna(row.get('Rating H&M')):
                try:
                    rating = float(row['Rating H&M'])
                    if rating > 4:
                        score += 0.1
                        positive_reasons.append(f'Высокий рейтинг H&M: {rating}')
                    else:
                        negative_reasons.append(f'Низкий рейтинг H&M: {rating}')
                except:
                    pass

        final_reasons = []
        if positive_reasons:
            final_reasons.append("Положительные факторы: " + "; ".join(positive_reasons))
        if negative_reasons:
            final_reasons.append("Отрицательные факторы: " + "; ".join(negative_reasons))
        
        return {
            'Decision': 'YES' if score >= 0.6 else 'NO',
            'Score': round(score, 2),
            'Reasons': " | ".join(final_reasons) + f" (Итоговая оценка: {score:.2f}/1.00)"
        }

def load_training_files():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('training_files', [])
    return []

def save_training_files(files):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'training_files': files}, f)

def process_file(input_path, output_path, training_files=None):
    print("\nИнициализация анализатора...")
    analyzer = ClothingAnalyzer()
    
    if training_files:
        analyzer.train_on_existing_data(training_files)
    
    print("\nЧтение входного файла...")
    df = pd.read_excel(input_path)
    print(f"Загружено {len(df)} товаров для анализа")
    
    print("\nНачало анализа товаров...")
    results = []
    for idx, row in df.iterrows():
        if idx % 10 == 0:
            print(f"Обработано {idx} товаров из {len(df)}")
        result = analyzer.analyze_item(row)
        results.append(result)
    
    df['Decision'] = [r['Decision'] for r in results]
    df['Score'] = [r['Score'] for r in results]
    df['Reasons'] = [r['Reasons'] for r in results]
    
    yes_count = sum(1 for r in results if r['Decision'] == 'YES')
    print(f"\nРезультаты анализа:")
    print(f"Всего товаров: {len(df)}")
    print(f"Рекомендовано к покупке (YES): {yes_count}")
    print(f"Не рекомендовано (NO): {len(df) - yes_count}")
    
    print("\nСохранение результатов...")
    df.to_excel(output_path, index=False)
    return df

if __name__ == "__main__":
    input_file = input("Введите путь к входному файлу Excel: ")
    output_file = input("Введите путь для сохранения результатов (включая имя файла.xlsx): ")
    
    training_files = load_training_files()
    if not training_files:
        training_files_input = input("Введите пути к файлам для обучения через запятую: ")
        training_files = [f.strip() for f in training_files_input.split(',')] if training_files_input else None
        save_training_files(training_files)
    
    results_df = process_file(input_file, output_file, training_files)
    print(f"Анализ завершен. Результаты сохранены в {output_file}")