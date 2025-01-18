from groq import Groq
import os
# from config import GROQ_API_KEY #to import from config .py
import json
import re
from embeddings import search_knowledge_base
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


class AIKeywordExtractor:
    def __init__(self, prompt: str):

        self.prompt = prompt

    def extract_keywords(self, prompt: str):
        results = search_knowledge_base(prompt, top_k=5)

        if results:

            items = [
                f"{item['name']} {', '.join(item['category'])} {item['description']}" for item in results]
            engineered_prompt = (
                f"You're a customer service worker. Your job is to suggest products based on their need and storage."
                f"Your task is to generate keywords for me. Remember, keywords only.\n"
                f"Consider the following as storage:\n{items}.\n"
                f"Extract the most relevant keywords from the following prompt: '{prompt}'.\n"
                f"Ensure the keywords align with available product categories, descriptions, and names in the storage.\n"
                f"Do not include any keywords that are not in the storage.\n"
                f"Do not generate any additional text, description, or explanation.\n"
                f"Number of keywords: minimum 1, maximum 4.\n"
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": engineered_prompt,
                    }
                ],
                model="llama-3.2-1b-preview",
            )

            response = chat_completion.choices[0].message.content

            removed_ordering = re.sub(r'\d+\.\s*', '', response).strip()
            raw_keywords = re.split(r'[,\n]', removed_ordering)

            keywords = []
            for kw in raw_keywords:
                kw = kw.strip()
                keywords.append(kw)
            return keywords[:5]


def main():

    user_prompt = "I am looking for a lightweight laptop with good battery life."
    extractor = AIKeywordExtractor(user_prompt)

    keywords = extractor.extract_keywords(user_prompt)
    print(f"Keywords: {keywords}")


if __name__ == "__main__":
    main()
