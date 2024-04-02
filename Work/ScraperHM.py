from bs4 import BeautifulSoup
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
# url = "https://www2.hm.com/en_us/productpage.0685816185.html"
url = 'https://www2.hm.com/en_us/productpage.1213473001.html'

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')

    product_color_article = soup.find('div', class_ = 'product-colors')
    product_name_price = soup.find('section', class_ = 'product-name-price')
    reviews_section = soup.find('div', class_ = 'details parbase')
    product = soup.find('div', class_ = 'product parbase').find_all('hm-product-reviews-summary-w-c')
    print(product)

    if product_color_article:
        #Title and price
        title = product_name_price.find('h1').text.strip()
        price = product_name_price.find('span').text.strip()

        #Color articul
        anchor = product_color_article.find('a')
        color = anchor['data-color']
        artile = anchor['data-articlecode']

        #Description
        description = reviews_section.find_all('p', limit=1)[0].text

        #Materials
        elements_for_materials = reviews_section.find(id = 'section-materialsAndSuppliersAccordion').find('ul').find_all(['h4','p'])
        text_list = [element.text for element in elements_for_materials]
        joined_text_for_materials = " ".join(text_list)

        #Size
        size_model = reviews_section.find('dl').find('div').text.strip().replace('\n', ': ')
        size = reviews_section.find('dl').find_all('div')[1].text.strip().replace('\n', ' ')
        

        print('------test------')
        print(f'Title: {title}')
        print(f'Price: {price}')
        print('Color:', color)
        print('Article: ', artile)
        print(f'Description: {description}')
        print(f'Materials: {joined_text_for_materials}')
        print(f'Size model: {size_model}')
        print(f'Size: {size}')
        print('----------------')
    else:
        print("not found")

except requests.exceptions.RequestException as e:
    print(f"Error ----> {e}")
except Exception as e:
    print(f'unexpected error {e}')