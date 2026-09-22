"""Imports"""
from pathlib import Path
import json
from knowledge.document import Document

"""Document Registry"""
document_registry = {}

"""Functions"""
def find_document(source: str) -> Document | None:
    """Searches document_registry using source and return corresponding Document"""
    return document_registry.get(source)

def register_document(document: Document) -> None:
    """Updates the document_registry with the given document. If the document already exists, updates its version and hash."""
    document_registry[document.source] = document
    
def is_document_registered(source: str) -> bool:
    return source in document_registry

def get_document_status(source: str) -> str:
    """Returns the status of the document whether it's available in the registry or not"""
    return "existing" if source in document_registry else "new"

def has_content_changed(existing_hash: str, new_hash: str) -> bool:
    """Returns True/False if existing hash and new hash doesnt match"""
    return existing_hash != new_hash

def get_processing_status(source: str, new_hash: str) -> str:
    """Returns new/changed/unchanged depending on the processing status"""
    if not is_document_registered(source):
        return "new"
    
    existing_document = find_document(source)
    
    if existing_document is None:
        return "new"
    
    if has_content_changed(existing_document.content_hash, new_hash):
        return "changed"
    
    return "unchanged"

def update_document(document: Document, new_hash: str) -> None:
    """Update's the document's version and content hash if the content has changed."""
    document.version += 1
    document.content_hash = new_hash
    
def save_document_registry(path: Path) -> None:
    """Saves the in-memory document_registry onto the manifest.json file"""
    data = {}
    
    for source, document in document_registry.items(): #converts document object into a dictionary
        data[source] = {
            "document_id": document.document_id,
            "source": document.source,
            "content_hash": document.content_hash,
            "version": document.version
        }
        
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
def load_document_registry(path: Path) -> None:
    """Loads back the manifest.json file data onto the document_registry"""
    if not path.exists():
        return
    
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        
    document_registry.clear() #to avoid merging with stale in-memory entries
    
    for source, document_data in data.items():
        document_registry[source] = Document(
            document_id=document_data["document_id"],
            source=document_data["source"],
            content_hash=document_data["content_hash"],
            version=document_data["version"]
        )