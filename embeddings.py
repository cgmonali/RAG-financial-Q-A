import os
from dotenv import load_dotenv
from typing import List
from openai import OpenAI
import cohere

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
COHERE_KEY = os.getenv("COHERE_API_KEY")

openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None
cohere_client = cohere.Client(COHERE_KEY) if COHERE_KEY else None

def get_embedding(text: str, input_type: str = "search_document") -> List[float]:
    """Generate embeddings using OpenAI or Cohere with fallback"""
    if openai_client:
        try:
            resp = openai_client.embeddings.create(
                model="text-embedding-3-small", input=text
            )
            return resp.data[0].embedding
        except Exception as e:
            print(f"[WARN] OpenAI failed ({e}), falling back to Cohere...")

    if cohere_client:
        resp = cohere_client.embed(
            texts=[text],
            model="embed-english-light-v3.0",
            input_type=input_type
        )
        return resp.embeddings[0]

    raise ValueError("No embedding provider available (OpenAI and Cohere missing/failing)")
