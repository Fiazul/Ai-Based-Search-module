import os
import sqlite3

"""
I collected some images from random sites using selenium. Just for demo images. 
So there were times when i got error in the middle of the process. So i had to erase the data and start again.
I created different table for it. it wont effect the other tables :D
"""


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
