import sqlite3


def update_specific_url(old_url, new_url):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET url = ? WHERE url = ?",
                   (new_url, old_url))
    conn.commit()
    conn.close()
    print(f"URLs have been updated from {old_url} to {new_url}.")


if __name__ == "__main__":
    old_url = "https://www.mobiledokan.com/"
    new_url = "https://gadgetandgear.com/category/phone"
    try:
        update_specific_url(old_url, new_url)
    except Exception as e:
        print(f"An error occurred: {e}")
