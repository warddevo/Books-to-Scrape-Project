import requests
import os
from bs4 import BeautifulSoup
url = "https://books.toscrape.com"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


# Folder where images will be saved
SAVE_FOLDER = r"C:\Users\wardd\OneDrive\Desktop\Open Classrooms\Use Python Basics for Market Analysis\Web Scraping\Images"

# Get Category URLs
categories = soup.find("div", class_="side_categories")
category_urls = []

for a in categories.find_all("a"):
    href = a["href"]
    if href.startswith("catalogue/category/books/"):
        full_url = url + "/" + href
        category_urls.append(full_url)


# Function: Get all book URLs in a category
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


# Function: Extract image URL from a book
def get_book_image_url(book_url):
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, "html.parser")

    img_tag = soup.find("img")
    src = img_tag["src"].replace("../../", "")
    full_image_url = url + "/" + src

    return full_image_url


# Function: Download an image
def download_image(image_url, filename):
    response = requests.get(image_url)
    filepath = os.path.join(SAVE_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"Saved: {filepath}")


# Scrape all books and download images
all_books = []

for category_url in category_urls:
    print(f"\nScraping category: {category_url}")
    book_urls = get_books_from_category(category_url)

    for book_url in book_urls:
        print(f"  Processing book: {book_url}")

        # Get image URL
        image_url = get_book_image_url(book_url)

        # Create filename from book URL
        filename = book_url.split("/")[-2] + ".jpg"

        # Download image
        download_image(image_url, filename)
