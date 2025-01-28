# image_analyzer.py
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

class ImageAnalyzer:
    def __init__(self):
        self.image_model = ResNet50(weights='imagenet')

    def analyze_image(self, url):
        """Анализирует изображение и возвращает характеристики"""
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