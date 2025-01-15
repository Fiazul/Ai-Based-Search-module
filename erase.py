import os
import sqlite3


def delete_image_paths():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT image_path FROM url_images")
    rows = cursor.fetchall()

    for row in rows:
        image_path = row[0]
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted file: {image_path}")

    # Clear the url_images table
    cursor.execute("DELETE FROM url_images")
    conn.commit()

    conn.close()
    print("All image paths have been deleted from the database.")


if __name__ == "__main__":
    delete_image_paths()
