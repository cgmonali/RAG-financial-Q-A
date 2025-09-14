import json
from ingestion import load_html_texts
from chunking import chunk_text
from embeddings import get_embedding
from vectorstore import VectorStore
from qa import answer_query

def build_vectorstore(docs):
    print("Building vector store...")
    first_emb = get_embedding("test")
    store = VectorStore(dim=len(first_emb))

    for name, text in docs.items():
        chunks = chunk_text(text)
        for idx, ch in enumerate(chunks):
            try:
                emb = get_embedding(ch, input_type="search_document")
                parts = name.split("_")
                company = parts[0].capitalize()
                year = parts[1] if len(parts) > 1 else "unknown"
                meta = {
                    "doc": name,
                    "company": company,
                    "year": year,
                    "chunk": ch,
                    "page": idx
                }
                store.add(emb, meta)
            except Exception as e:
                print(f"[WARN] Skipping chunk {idx} of {name}: {e}")

    print(f"✅ Added {len(store.metadata)} chunks to vector store")
    return store

def main():
    docs = load_html_texts("files")
    store = build_vectorstore(docs)

    print("RAG system ready! Enter your questions (type 'exit' to quit).")
    while True:
        q = input("\nYour question: ")
        if q.lower() in ["exit", "quit"]:
            break
        result = answer_query(q, store)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
