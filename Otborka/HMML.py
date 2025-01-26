import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

class ClothingAnalyzer:
   def __init__(self):
       self.image_model = ResNet50(weights='imagenet')
       
       self.basic_colors = [
           'Black', 'White', 'Grey', 'Navy', 'Beige', 'Dark blue', 
           'Light grey', 'Dark grey', 'Cream', 'Light beige', 'Off-white'
       ]
       
       self.basic_categories = [
           'T-shirt', 'Top', 'Socks', 'Leggings', 'Underwear', 'Bra',
           'Briefs', 'Knickers', 'Tank top', 'Basic T-shirt', 'Basic top'
       ]
       
       self.exclude_categories = [
           'Eyebrow pencil', 'Lipstick', 'Mascara', 'Foundation',
           'Concealer', 'Powder', 'Blush', 'Eyeshadow', 'Wash bag',
           'Makeup bag', 'Cosmetic bag'
       ]
       
       self.bad_bra_sizes = [
           '70A', '70E', '70F', '75A', '75E', '75F',
           '80A', '80E', '80F', '85A', '85E', '85F',
           '90A', '90E', '90F', '95A', '95E', '95F'
       ]
       
   def calculate_margin(self, client_price, euro_rate=105.0):
       return (client_price * 1.35 + 0.5) * euro_rate
       
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
                        
           return {'basic': is_basic, 'kids': is_kids}
       except:
           return {'basic': False, 'kids': False}

   def check_size(self, size, category, gender):
       size_str = str(size).upper()
       
       if ('XS' in size_str or 'XXS' in size_str) and 'KIDS' not in str(gender).upper():
           return False, "Размер XS/XXS - низкий спрос"
           
       if category == 'Trousers' and gender == 'Women':
           if size in ['32', '34'] or 'XS' in size_str or 'XXS' in size_str:
               return False, "Маленький размер для женских брюк"
               
       if gender == 'Men':
           if 'XS' in size_str:
               return False, "Размер XS для мужской одежды - низкий спрос"
               
       if category == 'Shoes' and gender == 'Men':
           try:
               size_num = float(size)
               if size_num < 41:
                   return False, f"Маленький размер мужской обуви ({size})"
           except:
               pass
               
       if category == 'Bra':
           if size in self.bad_bra_sizes:
               return False, f"Непопулярный размер бюстгальтера ({size})"
               
       return True, "Стандартный размер"

   def analyze_item(self, row):
       score = 0
       reasons = []
       
       if row['Category'] in self.exclude_categories:
           return {
               'Decision': 'NO',
               'Score': 0.1,
               'Reasons': f"Категория {row['Category']} исключена из рассмотрения"
           }
           
       size_ok, size_reason = self.check_size(row['Size'], row['Category'], row.get('Gender', ''))
       if not size_ok:
           return {
               'Decision': 'NO',
               'Score': 0.2,
               'Reasons': size_reason
           }
           
       qty = float(row['QTY']) if pd.notna(row['QTY']) else 0
       if qty > 2:
           score += 0.3
           reasons.append(f'Достаточное количество: {qty} шт.')
           
       if pd.notna(row['х2']):
           x2 = float(row['х2'])
           if x2 > 2:
               score += 0.2
               reasons.append(f'Хороший x2: {x2:.2f}')
       else:
           try:
               rrp = float(row['RRP. EUR*'])
               client_price = float(row['Client'])
               margin = self.calculate_margin(client_price)
               if margin < rrp * 0.7:
                   score += 0.2
                   reasons.append(f'Потенциальная маржа: {margin:.2f}€ при RRP {rrp}€')
           except:
               pass
           
       if any(color.lower() in str(row['Color']).lower() for color in self.basic_colors):
           score += 0.1
           reasons.append(f'Базовый цвет: {row["Color"]}')
           
       if row['Category'] in self.basic_categories:
           score += 0.1
           reasons.append(f'Базовая категория: {row["Category"]}')
           
       if 'cashmere' in str(row.get('Description', '')).lower():
           score += 0.15
           reasons.append('Кашемир')
           
       is_kids = 'kids' in str(row.get('Description', '')).lower() or 'children' in str(row.get('Description', '')).lower()
       if is_kids:
           score += 0.1
           reasons.append('Детский товар')
           if pd.notna(row.get('Rating H&M')):
               rating = float(row['Rating H&M'])
               if rating > 4:
                   score += 0.1
                   reasons.append(f'Высокий рейтинг H&M: {rating}')
                   
       if pd.notna(row['Photo link Parsing']):
           image_analysis = self.analyze_image(row['Photo link Parsing'])
           if image_analysis['basic']:
               score += 0.1
               reasons.append('Базовая модель (анализ фото)')
           if image_analysis['kids'] and is_kids:
               score += 0.1
               reasons.append('Подтверждено детское фото')
               
       return {
           'Decision': 'YES' if score >= 0.6 else 'NO',
           'Score': round(score, 2),
           'Reasons': '; '.join(reasons) + f" (Итоговая оценка: {score:.2f}/1.00)"
       }

def process_file(input_path, output_path):
   analyzer = ClothingAnalyzer()
   df = pd.read_excel(input_path)
   
   results = []
   for _, row in df.iterrows():
       result = analyzer.analyze_item(row)
       results.append(result)
   
   df['Decision'] = [r['Decision'] for r in results]
   df['Score'] = [r['Score'] for r in results]
   df['Reasons'] = [r['Reasons'] for r in results]
   
   df.to_excel(output_path, index=False)
   return df

if __name__ == "__main__":
   input_file = input("Введите путь к входному файлу Excel: ")
   output_file = input("Введите путь для сохранения результатов (включая имя файла.xlsx): ")
   results_df = process_file(input_file, output_file)
   print(f"Анализ завершен. Результаты сохранены в {output_file}")