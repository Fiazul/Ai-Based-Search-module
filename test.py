# # import json
# # import sqlite3

# # # Read JSON data from product_description.json
# # with open('knowledge_base.json', 'r') as json_file:
# #     product_data = json.load(json_file)

# # # Read URLs from urls.txt
# # with open('urls.txt', 'r') as url_file:
# #     urls = [line.strip() for line in url_file.readlines()]

# # # Assign each JSON object to a URL in order
# # assigned_data = []
# # for i, product in enumerate(product_data):
# #     if i < len(urls):
# #         assigned_data.append({
# #             "url": urls[i],
# #             "details": product
# #         })

# # # Assign the last URL to product_details.json
# # if urls:
# #     last_url = urls[-1]
# #     with open('knowledge_base.json', 'r') as details_file:
# #         product_details = json.load(details_file)
# #     assigned_data.append({
# #         "url": last_url,
# #         "details": product_details
# #     })

# # # Insert the data into the database
# # conn = sqlite3.connect("database.db")
# # cursor = conn.cursor()

# # for data in assigned_data:
# #     cursor.execute("INSERT INTO products (url, details) VALUES (?, ?)",
# #                    (data["url"], json.dumps(data["details"])))

# # conn.commit()
# # conn.close()

# # print("Data has been successfully inserted into the database.")
# import sqlite3


# def check_database():
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM url_images")
#     rows = cursor.fetchall()

#     for row in rows:
#         print(row)

#     conn.close()


# if __name__ == "__main__":
#     check_database()
