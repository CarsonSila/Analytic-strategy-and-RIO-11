"""RAG Engine for Operational Runbooks and Knowledge Base Search."""
import os
from pathlib import Path
from typing import List, Dict, Any
from src.config import config

class RunbookRAGEngine:
    """Lightweight retrieval-augmented generation engine over ops runbooks."""

    def __init__(self, runbooks_dir: Path | None = None):
        self.runbooks_dir = runbooks_dir or config.RUNBOOKS_PATH
        self.documents: List[Dict[str, Any]] = []
        self._load_runbooks()

    def _load_runbooks(self):
        """Index all markdown runbooks from the runbooks directory."""
        self.documents = []
        if not self.runbooks_dir.exists():
            return

        for file_path in self.runbooks_dir.glob("*.md"):
            try:
                content = file_path.read_text(encoding="utf-8")
                title = file_path.stem.replace("_", " ").title()
                # Parse headings and sections
                self.documents.append({
                    "filename": file_path.name,
                    "title": title,
                    "content": content,
                    "path": str(file_path),
                })
            except Exception:
                pass

    def retrieve_relevant_docs(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Find most relevant runbooks based on token relevance and semantic overlap."""
        if not self.documents:
            self._load_runbooks()

        query_tokens = set(query.lower().split())
        scored_docs = []

        for doc in self.documents:
            score = 0
            doc_lower = doc["content"].lower()
            title_lower = doc["title"].lower()

            for token in query_tokens:
                if len(token) <= 2:
                    continue
                if token in title_lower:
                    score += 5
                score += doc_lower.count(token)

            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k] if score > 0] or (self.documents[:top_k] if self.documents else [])

    def answer_query(self, query: str) -> Dict[str, Any]:
        """Answer an operational question with synthesized response and citations."""
        relevant_docs = self.retrieve_relevant_docs(query, top_k=2)

        if not relevant_docs:
            return {
                "answer": "No relevant operational runbooks were found matching your query. Try searching for topics like 'database failover', 'API latency', 'auth outage', or 'Stripe timeout'.",
                "sources": [],
            }

        # If OpenAI key is set, attempt LLM RAG synthesis
        if config.OPENAI_API_KEY:
            try:
                import requests
                context = "\n\n".join([f"=== Document: {d['title']} ({d['filename']}) ===\n{d['content']}" for d in relevant_docs])
                prompt = f"""You are an Operations Copilot. Answer the following query using ONLY the provided runbook context:
Context:
{context}

User Question: {query}

Provide a concise, direct, operational answer with bullet points and command snippets where appropriate."""
                headers = {"Authorization": f"Bearer {config.OPENAI_API_KEY}", "Content-Type": "application/json"}
                payload = {
                    "model": config.DEFAULT_AI_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2
                }
                resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
                resp.raise_for_status()
                ai_answer = resp.json()["choices"][0]["message"]["content"]
                return {
                    "answer": ai_answer,
                    "sources": [d["filename"] for d in relevant_docs],
                }
            except Exception:
                pass

        # Offline Intelligent Semantic Extractor
        primary_doc = relevant_docs[0]
        summary = f"Based on **{primary_doc['title']}** (`{primary_doc['filename']}`):\n\n"
        
        # Extract triage or mitigation sections
        lines = primary_doc["content"].split("\n")
        extracted_sections = []
        capture = False
        current_section = []

        for line in lines:
            if line.startswith("## "):
                if current_section:
                    extracted_sections.append("\n".join(current_section))
                    current_section = []
                capture = True
            if capture:
                current_section.append(line)
        if current_section:
            extracted_sections.append("\n".join(current_section))

        if extracted_sections:
            summary += "\n\n".join(extracted_sections[:2])
        else:
            summary += primary_doc["content"][:600] + "..."

        return {
            "answer": summary,
            "sources": [d["filename"] for d in relevant_docs],
        }

rag_engine = RunbookRAGEngine()

