"""Document and its identity"""

"""Imports"""
from dataclasses import dataclass
import hashlib, uuid

"""Creates a Document class with attributes for document ID, source, content hash, and version. It also includes functions to generate a unique document ID, calculate the hash of a string, and create a new Document instance."""
@dataclass
class Document:
    document_id: str
    source: str
    content_hash: str
    version: int 
    
def generate_document_id() -> str:
    """Generates a unique document ID using UUID4."""
    return str(uuid.uuid4())

def calculate_hash(input_string: str) -> str:
    """Calculates the SHA-256 hash of the input string."""
    hashlib_object = hashlib.sha256(input_string.encode("utf-8"))
    return hashlib_object.hexdigest()

def create_document(source: str, content_hash: str) -> Document:
    """Creates a new Document instance with a unique ID and version 1."""
    return Document(
        document_id=generate_document_id(),
        source=source,
        content_hash=content_hash,
        version=1
    )