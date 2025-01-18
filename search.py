from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from q_to_k import AIKeywordExtractor
from typing import List, Dict
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import JSONResponse
app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def create_database():
    """Creates the SQLite database and table if they do not exist."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        details JSON NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS url_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        image_path TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


create_database()

# Pydantic models


class ProductInput(BaseModel):
    url: str
    details: dict  # JSON-like structure


class SearchInput(BaseModel):
    input_type: str


@app.post("/add-product/")
def add_product(product: ProductInput):
    """Endpoint to add a product to the database."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (url, details) VALUES (?, ?)",
                       (product.url, json.dumps(product.details)))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error inserting product.")
    finally:
        conn.close()
    return {"message": "Product added successfully."}


@app.get("/products/")
def list_products():
    """Endpoint to list all products."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, details FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"url": row[0], "details": json.loads(row[1])} for row in rows
    ]


@app.post("/search/", response_class=JSONResponse)
def search(input_data: SearchInput):

    user_prompt = input_data.input_type
    extractor = AIKeywordExtractor(user_prompt)
    keywords = extractor.extract_keywords(user_prompt)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    results = []
    for keyword in keywords:

        query = "SELECT url, details FROM products WHERE details LIKE ?"
        cursor.execute(query, (f"%{keyword}%",))
        rows = cursor.fetchall()
        for row in rows:
            url = row[0]
            cursor.execute(
                "SELECT image_path FROM url_images WHERE url = ?", (url,))
            image_rows = cursor.fetchall()
            images = [
                f"{os.path.join(*image_row[0].split(os.sep))}" for image_row in image_rows]

            details = row[1]

            results.append({"url": url, "images": images, "details": details})

    conn.close()

    return JSONResponse(content={"results": results})


@ app.get("/show-images", response_class=HTMLResponse)
def show_images():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT url, image_path FROM url_images")
    rows = cursor.fetchall()

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Images from Database</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            .image-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            .image-item {
                margin: 10px;
                text-align: center;
            }
            .image-item img {
                max-width: 200px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="image-container">
    """

    for row in rows:
        url, image_path = row
        formatted_image_path = os.path.join(*image_path.split(os.sep))
        html_content += f"""
        <div class="image-item">
            <a href="{url}" target="_blank">
                <img src="{formatted_image_path}" alt="{url}">
            </a>
        </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    conn.close()
    return HTMLResponse(content=html_content)
