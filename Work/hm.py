import requests
from bs4 import BeautifulSoup

# User-Agent header for mimicking a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

def get_product_info(url):
  """Fetches and parses product information from the given URL.

  Args:
      url: The URL of the product page.

  Returns:
      A dictionary containing product details like name, price, color, etc.,
      or None if the request fails.
  """

  # Send request and handle errors
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise exception for non-200 status codes
  except requests.exceptions.RequestException as e:
    print(f"Error retrieving product info: {e}")
    return None

  # Parse HTML content
  soup = BeautifulSoup(response.content, 'html.parser')

  # Extract product details using more concise selectors
  product_details = {}
  product_details['name'] = soup.find('hm-product-name', id="js-product-name").text.strip()
  product_details['price'] = soup.find('div', class_="e26896").text.strip()  # Assuming price within this class
  product_colors = soup.find('div', class_="product-colors")
  if product_colors:
      color_label = product_colors.find_previous_sibling('h3', class_="product-input-label")
      if color_label:
          product_details['color'] = color_label.text.strip()

  # Add more selectors for other details (description, materials, etc.)
  # ... (refer to website structure for appropriate selectors)

  return product_details

# Example usage
url = "https://www2.hm.com/en_us/productpage.1003662002.html"
product_info = get_product_info(url)

if product_info:
  print("Product Name:", product_info['name'])
  print("Price:", product_info['price'])
  if 'color' in product_info:
      print("Color:", product_info['color'])
  # ... (print other details)
else:
  print("Failed to extract product information.")
