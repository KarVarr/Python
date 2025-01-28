# clothing_analyzer.py
import pandas as pd
from image_analyzer import ImageAnalyzer
from config import *

class ClothingAnalyzer:
    def __init__(self):
        self.image_analyzer = ImageAnalyzer()
        self.fragile_categories = FRAGILE_CATEGORIES
        self.reject_sizes = REJECT_SIZES
        self.allowed_small_bra = ALLOWED_SMALL_BRA
        self.bad_bra_sizes = BAD_BRA_SIZES
        self.basic_colors = BASIC_COLORS
        self.basic_categories = BASIC_CATEGORIES
        self.exclude_categories = EXCLUDE_CATEGORIES
        self.winter_categories = WINTER_CATEGORIES
        self.multi_item_categories = MULTI_ITEM_CATEGORIES
        self.curtain_min_size = CURTAIN_MIN_SIZE

    def train_on_existing_data(self, training_files):
        """Обучение на существующих данных"""
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

    def check_size(self, size, category, gender):
        """Проверяет размер на соответствие критериям"""
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
        """Анализирует отдельный товар"""
        try:
            score = 0
            positive_reasons = []
            negative_reasons = []
            
            # Проверка обязательных полей
            required_fields = ['Category', 'Size', 'QTY']
            missing_fields = [field for field in required_fields if pd.isna(row.get(field))]
            if missing_fields:
                return {
                    'Decision': 'NO',
                    'Score': 0.0,
                    'Reasons': f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"
                }

            # Проверка размеров XS/XXS
            if pd.notna(row.get('Size')):
                size_str = str(row['Size']).upper()
                if 'XS' in size_str or 'XXS' in size_str:
                    return {
                        'Decision': 'NO',
                        'Score': 0.0,
                        'Reasons': f"Отклонено: размер {size_str} не подходит для продажи"
                    }

            # Проверка категории
            if pd.notna(row.get('Category')):
                if row['Category'] in self.exclude_categories:
                    return {
                        'Decision': 'NO',
                        'Score': 0.0,
                        'Reasons': f"Отклонено: категория {row['Category']} исключена из рассмотрения"
                    }

            # Анализ маржинальности
            if pd.notna(row.get('RRP')) and pd.notna(row.get('sebes')):
                try:
                    rrp = float(row['RRP'])
                    cost = float(row['sebes'])
                    
                    rrp_rub = rrp * 105  # Конвертируем в рубли
                    cost_rub = cost      # Себестоимость уже в рублях
                    
                    margin_percent = ((rrp_rub - cost_rub) / cost_rub) * 100
                    
                    # Изменяем логику проверки маржи
                    if margin_percent >= 199:  # Проверяем на маржу 200% (с небольшим допуском)
                        score += 0.2
                        positive_reasons.insert(0,
                            f'Хорошая маржа {margin_percent:.0f}%: RRP {rrp_rub:.0f}₽ > себестоимость {cost_rub:.0f}₽'
                        )
                    elif margin_percent <= 0:
                        score -= 0.2
                        negative_reasons.append(
                            f'Отрицательная маржа: RRP {rrp_rub:.0f}₽ меньше себестоимости {cost_rub:.0f}₽'
                        )
                    elif margin_percent < 50:  # Добавляем предупреждение о низкой марже
                        negative_reasons.append(
                            f'Низкая маржа {margin_percent:.0f}%: RRP {rrp_rub:.0f}₽ недостаточно выше себестоимости {cost_rub:.0f}₽'
                        )
               
                except ValueError as e:
                    print(f"Ошибка расчета маржи для артикула {row.get('Article ID')}: {str(e)}")
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

            # Анализ наличия нескольких предметов
            is_multi_item = False
            if pd.notna(row.get('Description')):
                is_multi_item = any(word in str(row['Description']).lower() 
                                 for word in self.multi_item_categories)
            item_multiplier = 2 if is_multi_item else 1
            
            if is_multi_item:
                score += 0.2
                positive_reasons.append('Набор предметов')

            # Анализ изображения
            if pd.notna(row.get('Photo link Parsing')):
                image_analysis = self.image_analyzer.analyze_image(row['Photo link Parsing'])
                if image_analysis['multi_item']:
                    item_multiplier = max(item_multiplier, image_analysis['item_count'])
                    positive_reasons.append(f'Набор из {item_multiplier} предметов (анализ фото)')
                if image_analysis['basic']:
                    score += 0.1
                    positive_reasons.append('Базовая модель (анализ фото)')
                if image_analysis['kids']:
                    score += 0.1
                    positive_reasons.append('Детский товар (подтверждено фото)')

            # Анализ x2
            if pd.notna(row.get('х2')):
                try:
                    x2 = float(row['х2'])  # Убрали умножение на item_multiplier
                    if x2 > 2:
                        score += 0.2
                        positive_reasons.append(f'Хороший x2: {x2:.2f}')
                    else:
                        negative_reasons.append(f'Низкий x2: {x2:.2f}')
                except ValueError as e:
                    print(f"Ошибка при анализе x2: {str(e)}")
                    negative_reasons.append('Ошибка при анализе x2')

            # Анализ цвета
            if pd.notna(row.get('Color')) and any(color.lower() in str(row['Color']).lower() 
                                                 for color in self.basic_colors):
                score += 0.1
                positive_reasons.append(f'Базовый цвет: {row["Color"]}')
            else:
                negative_reasons.append(f'Небазовый цвет: {row.get("Color", "Нет данных")}')

            # Проверка базовой категории
            if pd.notna(row.get('Category')) and row['Category'] in self.basic_categories:
                score += 0.1
                positive_reasons.append(f'Базовая категория: {row["Category"]}')

            # Проверка на кашемир
            if pd.notna(row.get('Description')) and 'cashmere' in str(row['Description']).lower():
                score += 0.15
                positive_reasons.append('Кашемир')

            # Проверка детского товара
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

            # Формирование итогового результата
            final_reasons = []
            if positive_reasons:
                # Сортируем positive_reasons так, чтобы причины с "маржой" были первыми
                margin_reasons = [r for r in positive_reasons if 'маржа' in r.lower()]
                other_reasons = [r for r in positive_reasons if 'маржа' not in r.lower()]
                sorted_reasons = margin_reasons + other_reasons
                final_reasons.append("Положительные факторы: " + "; ".join(sorted_reasons))
                
            if negative_reasons:
                final_reasons.append("Отрицательные факторы: " + "; ".join(negative_reasons))
            
            if not final_reasons:
                final_reasons = ["Недостаточно данных для анализа"]
                
            return {
                'Decision': 'YES' if score >= 0.6 else 'NO',
                'Score': round(score, 2),
                'Reasons': " | ".join(final_reasons) + f" (Итоговая оценка: {score:.2f}/1.00)"
            }
            
        except Exception as e:
            print(f"Ошибка при анализе товара: {str(e)}")
            return {
                'Decision': 'NO',
                'Score': 0.0,
                'Reasons': f"Ошибка анализа: {str(e)}"
            }