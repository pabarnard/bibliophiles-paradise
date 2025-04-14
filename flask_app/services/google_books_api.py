# This file will handle the Google Books API calls and return the raw data.
# NOTE: This file will in the future deal with errors in the API. 
import requests, os

GOOGLE_API_LINK = "https://www.googleapis.com/books/v1/volumes"

def get_books_by_isbn(form_data, id_set, shelf_ids):
    """Grabs books from Google Books API by ISBN - both 10- and 13-digit values

    Args:
        form_data (dict): Raw data from HTML form
        id_set (set(str)): Set of IDs saved as strings

    Returns:
        list: A list of dictionaries holding book data from the Google Books API
    """
    book_results = process_data({
        "api_key": os.getenv("GOOGLE_API_KEY"), 
        "q": "isbn:"+form_data["isbn"],
        "langRestrict": "en"
        }, id_set, shelf_ids)
    return book_results

def get_books_by_title_and_author(form_data, id_set, shelf_ids):
    """Grabs books from Google Books API by title and author

    Args:
        form_data (dict): Raw data from HTML form with "title" and "author" as keys
        id_set (set(str)): Set of IDs saved as strings

    Returns:
        list: A list of dictionaries holding book data from the Google Books API
    """
    book_results = process_data({
        "api_key": os.getenv("GOOGLE_API_KEY"), 
        "q": "intitle:"+form_data["title"]+"+"+"inauthor:"+form_data["author"],
        "langRestrict": "en"
        }, id_set, shelf_ids)
    return book_results

# Helper function to make API call, then process raw JSON data and convert it to a form that can be saved in the database
def process_data(query_data, all_volume_ids_in_db, shelf_volume_ids):
    r = requests.get(GOOGLE_API_LINK, query_data)
    raw_json = r.json()
    all_books = {} # Dictionary where each key is a Google Volume ID with info about the book
    for book in raw_json['items']:
        book_info = book['volumeInfo']
        # Take data from API and put it in new dictionary that's usable in case it's saved to the local databsase
        clean_book_dict = {}
        google_volume_id = book['id'] if 'id' in book else ""
        # Boolean variables for if this book is already in the database and if this book is in the logged in user's shelf
        clean_book_dict["is_in_db"] = google_volume_id in all_volume_ids_in_db
        clean_book_dict["is_in_users_shelf"] = True if clean_book_dict["is_in_db"] and google_volume_id in shelf_volume_ids else False
        clean_book_dict["title"] = book_info['title'] if 'title' in book_info else ""
        if "authors" in book_info:
            all_authors = ""
            for author in book_info['authors']:
                if all_authors != "":
                    all_authors += ", "
                all_authors += author
            clean_book_dict["authors"] = all_authors
        else:
            clean_book_dict["authors"] = ""
        clean_book_dict["publication_date"] = book_info['publicationDate'] if 'publicationDate' in book_info else ""
        clean_book_dict["page_count"] = book_info['pageCount'] if 'pageCount' in book_info else ""
        if "imageLinks" in book_info:
            clean_book_dict["thumbnail"] = book_info["imageLinks"]["thumbnail"] if "thumbnail" in book_info["imageLinks"] else ""
        else:
            clean_book_dict["thumbnail"] = ""
        if "industryIdentifiers" in book_info:
            for identifier in book_info["industryIdentifiers"]:
                if identifier["type"] == "ISBN_13":
                    clean_book_dict["isbn13"] = identifier["identifier"]
                    break
                elif identifier["type"] == "ISBN_10":
                    clean_book_dict["isbn13"] = "978"+identifier["identifier"] # Convert from ISBN10 to ISBN13
            if "isbn13" not in clean_book_dict:
                clean_book_dict["isbn13"] = ""
        else:
            clean_book_dict["isbn13"] = ""
        all_books[google_volume_id] = clean_book_dict
    return all_books