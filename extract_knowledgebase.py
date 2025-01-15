import sqlite3
import json


def extract_knowledge_base(output_file='knowledge_base.json'):
    """
    Extracts the details from the products table and saves them to a JSON file. 
    It is just a sample which worked for me. i will work on it.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT details FROM products")
    rows = cursor.fetchall()

    knowledge_base = [json.loads(row[0]) for row in rows]

    with open(output_file, 'w') as file:
        json.dump(knowledge_base, file, indent=4)

    conn.close()


if __name__ == "__main__":

    extract_knowledge_base()
