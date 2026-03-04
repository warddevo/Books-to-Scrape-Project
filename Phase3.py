import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#headers
headers = ["product_page_url" , "universal_product_code (upc)", "book_title" , "price_including_tax" , "price_excluding_tax" , "quantity_available" , "product_description" , "category" , "review_rating" , "image_url"] 


# --- Get all category URLs ---
categories = soup.find("div", class_="side_categories")
category_urls = []

for a in categories.find_all("a"):
    href = a["href"]
    if href.startswith("catalogue/category/books/"):
        full_url = url + "/" + href
        category_urls.append(full_url)


# --- Function to get all book URLs from a category ---
def get_books_from_category(category_url):
    book_urls = []
    next_page = category_url

    while next_page:
        page = requests.get(next_page)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract book links
        for h3 in soup.find_all("h3"):
            relative = h3.find("a")["href"]
            relative = relative.replace("../../../", "")
            full_book_url = url + "/catalogue/" + relative
            book_urls.append(full_book_url)

        # Check for next page
        next_button = soup.find("li", class_="next")
        if next_button:
            next_href = next_button.find("a")["href"]
            next_page = next_page.rsplit("/", 1)[0] + "/" + next_href
        else:
            next_page = None

    return book_urls


# Loop through each category and create a CSV
for category_url in category_urls:

    # Extract category name from URL
    category_strip = category_url.rstrip("/").split("/")[-2]
    category_name = category_strip.split("_")[0]

    # Get all book URLs for this category
    books = get_books_from_category(category_url)

    # CSV Filename
    filename = f"Phase3_{category_name}.csv"

    #Create CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)

        # Scrape each book in this category
        for book_url in books:
            page = requests.get(book_url)
            soup = BeautifulSoup(page.content, "html.parser")

            universal_product_code = soup.find("th", string="UPC").find_next_sibling("td").text
            book_title = soup.find("h1").text
            price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text
            price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text
            quantity_available = soup.find("th", string="Availability").find_next_sibling("td").text

            desc = soup.find("div", id="product_description")
            if desc:
                product_description = desc.find_next("p").text
            else:
                product_description = ""

            category = soup.find("ul", class_="breadcrumb").find_all("a")[2].get_text(strip=True)
            review_rating = soup.find("p", class_="star-rating")["class"][1]
            image_url = "https://books.toscrape.com/" + soup.find("div", class_="item active").img["src"].lstrip("../")
            writer.writerow([book_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, image_url])

    print(f"Saved {len(books)} books to {filename}\n")