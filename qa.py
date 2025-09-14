from typing import Dict
from .agent import decompose_query

def answer_query(query: str, store) -> Dict:
    sub_queries = decompose_query(query)
    reasoning = []
    sources = []

    for sq in sub_queries:
        results = store.search("financial metric: " + sq, top_k=3)
        if not results:
            results = store.search("reporting data: " + sq, top_k=3)

        reasoning.append(f"Sub-query: {sq}, found {len(results)} relevant chunks")
        for r in results:
            excerpt = r["chunk"][:200] + "..." if len(r["chunk"]) > 200 else r["chunk"]
            sources.append({
                "company": r.get("company", "unknown"),
                "year": r.get("year", "unknown"),
                "excerpt": excerpt,
                "page": r.get("page", -1)
            })

    answer = "No relevant chunks found"
    if sources:
        answer = f"Synthesized answer from {len(sources)} retrieved chunks"

    return {
        "query": query,
        "answer": answer,
        "reasoning": " -> ".join(reasoning),
        "sub_queries": sub_queries,
        "sources": sources
    }
