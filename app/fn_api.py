import json
import os
import requests
import subprocess
from fn_config import FnConfig
from models import Book, Category


class FnStore:
    CATEGORIES = None
    CATEGORY_CHOICES = None

    def load_categories():
        categories_arr = api_get_categories()
        FnStore.CATEGORY_CHOICES = [category.name for category in categories_arr]
        FnStore.CATEGORIES = {category.id: category.name for category in categories_arr}


def api_get_categories():
    response = requests.get(f"{FnConfig.API_URL}/categories")
    categories_data = json.loads(response.text)
    categories = [Category(**category) for category in categories_data]
    return categories


def api_search_books(name: str, category_id=None) -> list[Book]:
    req_data = {"name": name}
    if category_id:
        req_data["category_id"] = category_id
    reponse = requests.post(
        f"{FnConfig.API_URL}/books/search",
        data=req_data,
    )
    books_data = json.loads(reponse.text)
    books = [Book(**book) for book in books_data]
    return books


def api_update_book(id, name=None, category_id=None, price=None):
    data = {}
    if name:
        data["name"] = name
    if category_id:
        data["category_id"] = category_id
    if price:
        data["price"] = price
    response = requests.put(
        f"{FnConfig.API_URL}/books/{id}",
        data=data,
    )
    return response.status_code == 200


def api_create_category(name):
    response = requests.post(
        f"{FnConfig.API_URL}/categories/create",
        data={"name": name},
    )
    return json.loads(response.text)["id"]


def api_create_book(filename, price, category_id):
    name = os.path.basename(filename).split(".")[0]
    with open(filename, "rb") as file:
        response = requests.post(
            f"{FnConfig.API_URL}/books/create",
            files={"file": file},
            data={"price": price, "category_id": category_id, "name": name},
        )
    return response.status_code == 200


def api_download_book(book_id) -> None:
    response = requests.get(f"{FnConfig.API_URL}/books/{book_id}/download")
    subprocess.Popen(rf"explorer /select, {response.text}")
