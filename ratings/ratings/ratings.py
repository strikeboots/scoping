import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
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
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


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
    """
    Books to Scrape usually stores rating in something like:
    <p class="star-rating Three"></p>
    """
    rating_tag = article.select_one("p.star-rating")
    if not rating_tag:
        return 0

    classes = rating_tag.get("class", [])
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

            title = title_tag.get("title", "").strip() if title_tag else "No title"
            price = price_tag.get_text(strip=True) if price_tag else "No price"
            availability = availability_tag.get_text(strip=True) if availability_tag else "Unknown"
            rating = get_rating(article)

            books.append({
                "title": title,
                "rating": rating,
                "price": price,
                "availability": availability
            })

        next_link = soup.select_one("li.next a")
        if next_link:
            next_href = next_link.get("href")
            next_page = urljoin(next_page, next_href)
        else:
            next_page = None

    return books


def choose_genre(categories):
    genre_names = sorted(categories.keys())

    print("\nAvailable genres:")
    for i, genre in enumerate(genre_names, start=1):
        print(f"{i}. {genre}")

    while True:
        choice = input("\nPick a genre by number or exact name: ").strip()

        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(genre_names):
                return genre_names[num - 1], categories[genre_names[num - 1]]

        if choice in categories:
            return choice, categories[choice]

        print("Invalid choice. Try again.")


def main():
    print("Loading genres...")
    categories = get_categories()

    genre_name, genre_url = choose_genre(categories)

    print(f"\nScraping books from genre: {genre_name}")
    books = scrape_books_from_category(genre_url)

    books.sort(key=lambda book: book["rating"], reverse=True)

    print(f"\nBooks in '{genre_name}' sorted from highest to lowest rating:\n")

    for i, book in enumerate(books, start=1):
        print(
            f"{i}. {book['title']}\n"
            f"   Rating: {book['rating']} stars\n"
            f"   Price: {book['price']}\n"
            f"   Availability: {book['availability']}\n"
        )


if __name__ == "__main__":
    main()