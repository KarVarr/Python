from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
url = "https://www.dns-shop.ru/catalog/actual/e8ed5050-4901-4b48-81b5-1de1b6e2d321/?stock=now-today-tomorrow-later&category=295a14080bbc7fd7"

response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.content, 'lxml')
soup = BeautifulSoup(response.content, 'html.parser')

for item in soup.select('.container'):
    try:
        print('----------------')
        print(item)
        # print(item.find('h1', class_ = 'Heading-module--general__1cV9K ProductName-module--productTitle__3ryCJ Heading-module--small__6VQbz'))
        # print(item.select('#js-product-name')[0].get_text().strip())
        # print(item.select('.ProductName-module--container__3Qbt1')[0]['.Heading-module--general__1cV9K ProductName-module--productTitle__3ryCJ Heading-module--small__6VQbz'])
        # product_name = item.select('.product-detail-info__header-name')
        # print(f"Product Name: {product_name}")
        # print(item)
        # print(item.select('.ProductName-module--container__3Qbt1')[0]['.Heading-module--general__1cV9K'])
        # print(item.select('.item-image')[0]['data-altimage'])
        # print(item.select('.item-image')[0]['data-alttext'])
        # print(item.select('.item-price')[0].get_text().strip())


        # for swatch in item.select('.swatch'):
        #     print(swatch.get_text().strip())

    except Exception as e:
        #raise у
        print("")
