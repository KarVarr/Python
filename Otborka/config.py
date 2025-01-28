# config.py
CONFIG_FILE = 'ml_config.json'

# Базовые настройки для категорий
FRAGILE_CATEGORIES = [
    'Glass', 'Vase', 'Cup', 'Glass set', 'Plate set',
    'Bowl', 'Wine glass', 'Drinking glass', 'Ceramic'
]

REJECT_SIZES = {
    'general': ['XXS', 'XS'],
    'women_bottoms': ['32', '34'],
    'men': ['XS'],
    'women_shoes': ['35', '42'],
    'men_shoes': [str(i) for i in range(35, 41)]
}

ALLOWED_SMALL_BRA = ['70A', '75A']

BAD_BRA_SIZES = [
    '70E', '70F', '75E', '75F',
    '80A', '80E', '80F', '85A', '85E', '85F',
    '90A', '90E', '90F', '95A', '95E', '95F'
]

BASIC_COLORS = [
    'Black', 'White', 'Grey', 'Navy', 'Beige', 'Dark blue',
    'Light grey', 'Dark grey', 'Cream', 'Light beige', 'Off-white'
]

BASIC_CATEGORIES = [
    'T-shirt', 'Top', 'Socks', 'Leggings', 'Underwear', 'Bra',
    'Briefs', 'Knickers', 'Tank top', 'Basic T-shirt', 'Basic top'
]

EXCLUDE_CATEGORIES = [
    'Make-up bag', 'Cosmetic bag', 'Wash bag', 'Beauty box',
    'Eyebrow pencil', 'Lipstick', 'Mascara', 'Foundation',
    'Concealer', 'Powder', 'Blush', 'Eyeshadow'
]

WINTER_CATEGORIES = [
    'Jacket', 'Coat', 'Winter boots', 'Sweater', 'Cardigan',
    'Scarf', 'Gloves', 'Hat', 'Winter accessories'
]

MULTI_ITEM_CATEGORIES = ['Set', 'Pack', 'Kit', 'Bundle']
CURTAIN_MIN_SIZE = 120