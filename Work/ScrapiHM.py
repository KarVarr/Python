import requests
from lxml import html

# URL страницы для парсинга
url = "https://www2.hm.com/en_us/productpage.0685816185.html"

# Отправляем запрос на сервер и получаем содержимое страницы
response = requests.get(url)
html_content = response.content

# Создаем объект ElementTree из HTML-кода
tree = html.fromstring(html_content)

# Используем XPath для извлечения нужных данных
# Проверяем, найден ли элемент с указанным XPath-выражением
product_name_elements = tree.xpath('//h1[@class="Heading-module--general__1cV9K ProductName-module--productTitle__3ryCJ Heading-module--small__6VQbz"]/text()')
if product_name_elements:
    product_name = product_name_elements[0].strip()
    print("Название товара:", product_name)
else:
    print("Название товара не найдено")

# Аналогично можно получить другие данные, например цену товара:
price_elements = tree.xpath('//div[@class="primary-row product-item-price"]//span[@class="price"]/text()')
if price_elements:
    price = price_elements[0].strip()
    print("Цена товара:", price)
else:
    print("Цена товара не найдена")

# Можно продолжить извлечение других данных, таких как описание товара, изображения и т. д.



