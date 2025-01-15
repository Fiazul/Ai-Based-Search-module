import os
from config import colander
from groq import Groq
import base64

client = Groq(api_key=colander)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def colander_images(image_path):

    if not image_path or not os.path.exists(image_path):
        raise ValueError("NothingFound: No images found or invalid path")

    base64_image = encode_image(image_path)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You're a classifier. Please answer in binary if the following image is an actual physical product or not. "
                     "Your output should be 'yes' or 'no'. The image can be a logo, advertisement posters, or anything. "
                     "But only say 'yes' if it is a product image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )

    response = chat_completion.choices[0].message.content
    if response:
        if 'yes' in response.strip().lower():
            return image_path
        else:
            return None


# Example usage
if __name__ == "__main__":
    image_path = "E:\Ai-Based-Search-module\media\dd990998b6c065bee99c714d5639d7eb_image_7.jpg"
    result = colander_images(image_path)
    if result:
        print(f"Image '{result}' is classified as a product.")
    else:
        print("The image is not classified as a product.")
