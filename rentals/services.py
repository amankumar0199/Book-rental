import requests

OPENLIBRARY_URL = "https://openlibrary.org/search.json"


def fetch_book_from_openlibrary(title):
    response = requests.get(OPENLIBRARY_URL, params={"title": title})
    data = response.json()

    if response.status_code != 200:
        return None

    if not data["docs"]:
        return None

    book_data = data["docs"][0]

    page_count = (
        book_data.get("number_of_pages_median")
        or book_data.get("number_of_pages")
        or 100
    )

    return {
        "title": book_data.get("title"),
        "author": book_data.get("author_name", ["Unknown"])[0],
        "page_count": page_count,
    }
