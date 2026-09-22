"""imports"""

from dataclasses import dataclass, field
import random

"""functions"""
def generate_id():
    chunk_id_gen = random.randint(0, 5)
    return chunk_id_gen

@dataclass
class Chunk:
    text: str
    source: str
    document_id: str
    chunk_index: int
    chunk_id: str = field(default_factory=generate_id)
    
def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0")
    elif overlap >= chunk_size:
        raise ValueError("Overlap must be less than chunk size")
    elif overlap < 0:
        raise ValueError("Overlap must be greater than or equal to 0")
    
    chunked = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunked.append(chunk)
        start += step
    return chunked

def create_chunks(text: str, chunk_size: int, overlap: int, source: str, document_id: str) -> list[Chunk]:
    chunked_texts = chunk_text(text, chunk_size, overlap)
    final_chunks = []
    for i, chunk in enumerate(chunked_texts):
        chunk_obj = Chunk(
            text=chunk,
            source=source,
            chunk_index=i,
            document_id=document_id
        )
        final_chunks.append(chunk_obj)
    return final_chunks