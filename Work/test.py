import requests
from bs4 import BeautifulSoup

# Set a User-Agent header to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# Use a session object to maintain cookies and session data
with requests.Session() as session:
    session.headers.update(headers)
    
    link = "https://www2.hm.com/en_us/productpage.1003662002.html"
    response = session.get(link)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.find('main', class_ = "fluid")
        product_parbase = main.find('div', class_ = "product")
        layout = product_parbase.find('div', class_ = "layout")
        module = layout.find('div', class_ = "module")
        column2 = module.find('div', class_ = "column2")
        sub_content = column2.find('div', class_ = "sub-content")
        inner = sub_content.find('div', class_ = "inner")
        product_name_price = inner.find('section', class_ = "product-name-price")
        title = product_name_price.find('hm-product-name', id = "js-product-name").text
        print(title)

        price_parbase = product_name_price.find('div', class_ = "price")
        primaty_row = price_parbase.find('div', class_ = "primary-row")
        # price = primaty_row.find('hm-product-price', id = "product-price")
        # span_price = price.find('div', class_ = "e26896")
        # sp = price.find("div")
        # print(primaty_row)

        product_colors = column2.find('div', class_ = "product-colors")
        color = product_colors.find_previous_sibling('h3', class_ = "product-input-label").text
        print(f"color: {color}")


        delivery_information_wrapper = column2.find('div', id = "delivery-information-wrapper")
        test = delivery_information_wrapper.find('span')
        print(delivery_information_wrapper)

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)




