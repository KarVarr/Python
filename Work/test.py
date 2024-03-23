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
    
    # Make the request using the session object
    response = session.get(link)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Now you can continue processing the HTML content as needed
        # For example, print the title of the page
        print("Title:", soup.title.text)
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)





# user = fake_useragent.UserAgent().random
# header = {"user-agent": user}
# link = "https://www2.hm.com/en_us/productpage.1003662002.html"
# response = requests.get(link).text
# print(response)
# print(requests.get(link).status_code)

# soup = BeautifulSoup(response, "lxml")

# main = soup.find('body', class_ = "pdp-page not-signed-in using-mouse")
# app = main.find('div', id = 'content')
# title_header = app.find('div', class_ = "text")
# a = title_header.find('a', class_ = "title").text
# print(main)