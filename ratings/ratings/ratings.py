<<<<<<< HEAD
ï»¿import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

=======
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
>>>>>>> origin/main
START_URL = "https://books.toscrape.com/catalogue/category/books_1/index.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_soup(url):
    response = requests.get(url, timeout=10)
<<<<<<< HEAD
    response.encoding = "utf-8"
=======
>>>>>>> origin/main
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def clean_price(price_text):
    if not price_text:
        return "No price"
<<<<<<< HEAD
    return price_text.strip()
=======

    price_text = price_text.strip()
    price_text = price_text.replace("Â£", "£")
    price_text = price_text.replace("A£", "£")
    return price_text
>>>>>>> origin/main


def get_categories():
    soup = get_soup(START_URL)

    categories = {}
    category_links = soup.select("div.side_categories ul li ul li a")

    for link in category_links:
        name = link.get_text(strip=True)
        href = link.get("href")
        full_url = urljoin(START_URL, href)
        categories[name] = full_url

    return categories


def get_rating(article):
    rating_tag = article.select_one("p.star-rating")
<<<<<<< HEAD

=======
>>>>>>> origin/main
    if not rating_tag:
        return 0

    classes = rating_tag.get("class", [])
<<<<<<< HEAD

=======
>>>>>>> origin/main
    for class_name in classes:
        if class_name in RATING_MAP:
            return RATING_MAP[class_name]

    return 0


def scrape_books_from_category(category_url):
    books = []
    next_page = category_url

    while next_page:
        soup = get_soup(next_page)

        for article in soup.select("article.product_pod"):
            title_tag = article.select_one("h3 a")
            price_tag = article.select_one("p.price_color")
            availability_tag = article.select_one("p.instock.availability")

<<<<<<< HEAD
            title = title_tag.get("title", "").strip()
            price = clean_price(price_tag.get_text(strip=True))
            availability = availability_tag.get_text(strip=True)
=======
            title = title_tag.get("title", "").strip() if title_tag else "No title"
            raw_price = price_tag.get_text(strip=True) if price_tag else "No price"
            price = clean_price(raw_price)
            availability = availability_tag.get_text(strip=True) if availability_tag else "Unknown"
>>>>>>> origin/main
            rating = get_rating(article)

            books.append({
                "title": title,
                "rating": rating,
                "price": price,
                "availability": availability
            })

        next_link = soup.select_one("li.next a")
<<<<<<< HEAD

        if next_link:
            next_page = urljoin(next_page, next_link.get("href"))
=======
        if next_link:
            next_href = next_link.get("href")
            next_page = urljoin(next_page, next_href)
>>>>>>> origin/main
        else:
            next_page = None

    return books


def choose_genre(categories):
    genre_names = sorted(categories.keys())

    print("\nAvailable genres:")
    for i, genre in enumerate(genre_names, start=1):
        print(f"{i}. {genre}")

<<<<<<< HEAD
    while True:
        choice = input("\nPick a genre by number only: ").strip()

        if choice.isdigit():
            num = int(choice)

=======
    normalized_categories = {
        genre.strip().lower(): (genre, url)
        for genre, url in categories.items()
    }

    while True:
        choice = input("\nPick a genre by number or exact name: ").strip()

        if choice.isdigit():
            num = int(choice)
>>>>>>> origin/main
            if 1 <= num <= len(genre_names):
                selected_genre = genre_names[num - 1]
                return selected_genre, categories[selected_genre]

<<<<<<< HEAD
        print("Invalid number. Try again.")
=======
        normalized_choice = choice.lower()
        if normalized_choice in normalized_categories:
            return normalized_categories[normalized_choice]

        print("Invalid choice. Try again.")
>>>>>>> origin/main


def main():
    print("Loading genres...")
    categories = get_categories()

    genre_name, genre_url = choose_genre(categories)

    print(f"\nScraping books from genre: {genre_name}")
    books = scrape_books_from_category(genre_url)

    books.sort(key=lambda book: book["rating"], reverse=True)

    print(f"\nBooks in '{genre_name}' sorted from highest to lowest rating:\n")

    for i, book in enumerate(books, start=1):
<<<<<<< HEAD
        print(f"{i}. {book['title']}")
        print(f"   Rating: {book['rating']} stars")
        print(f"   Price: {book['price']}")
        print(f"   Availability: {book['availability']}")
        print()
=======
        print(
            f"{i}. {book['title']}\n"
            f"   Rating: {book['rating']} stars\n"
            f"   Price: {book['price']}\n"
            f"   Availability: {book['availability']}\n"
        )
>>>>>>> origin/main


if __name__ == "__main__":
    main()