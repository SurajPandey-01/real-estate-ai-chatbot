
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Real Estate AI Chatbot",
    },
)


def generate_answer(question: str, property_context: list):
    """
    Generate an answer using OpenRouter
    based on retrieved property information.
    """

    if not property_context:
        return "I couldn't find any matching properties in the available database."

    context = "\n\n".join([
        str(property_data)
        for property_data in property_context
    ])

    response = client.chat.completions.create(
        model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful real estate assistant. "
                    "Answer questions using only the property information "
                    "provided in the context. Do not invent prices, "
                    "locations, amenities, or completion dates. "
                    "If information is missing, say it is not available. "
                    "Mention the source of the property information."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Property information:\n{context}\n\n"
                    f"User question: {question}"
                ),
            },
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content
    