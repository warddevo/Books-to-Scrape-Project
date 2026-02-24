import requests
import csv
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/catalogue/category/books/music_14/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#headers
headers = ["product_page_url" , "universal_ product_code (upc)", "book_title" , "price_including_tax" , "price_excluding_tax" , "quantity_available" , "product_description" , "category" , "review_rating" , "image_url"] 

#lists
book_urls = [] 
for h3 in soup.find_all("h3"): 
    a_tag = h3.find("a") 
    relative_url = a_tag["href"] 
    full_url = "https://books.toscrape.com/catalogue/" + relative_url.replace("../../../", "") # join with base URL 
    book_urls.append(full_url)

#extract data and load to csv
with open('phase2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(headers)

    for books in book_urls:
        page = requests.get(books)
        soup = BeautifulSoup(page.content, 'html.parser')

        product_page_url = url
        universal_product_code = soup.find("th", string="UPC").find_next_sibling("td").text
        book_title = soup.find("h1").text
        price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text
        price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text
        quantity_available = soup.find("th", string="Availability").find_next_sibling("td").text
        product_description = soup.find("div", class_="sub-header", id="product_description").find_next("p").text
        category = soup.find("ul", class_="breadcrumb").find_all("a")[2].get_text(strip=True)
        review_rating = soup.find("p", class_="star-rating")["class"][1]
        image_url = "https://books.toscrape.com/" + soup.find("div", class_="item active").img["src"].lstrip("../")

        writer.writerow([product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, image_url])
        
