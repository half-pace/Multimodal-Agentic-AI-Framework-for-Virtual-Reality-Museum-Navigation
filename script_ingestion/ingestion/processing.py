"""Imports"""
from pathlib import Path
from extraction import extract_pdf_text
from cleaning import normalize_whitespace
from knowledge.document import calculate_hash, create_document
from ingestion.discovery import discover_files, get_relative_source
from ingestion.manifest import (
    find_document,
    get_processing_status,
    load_document_registry,
    register_document,
    save_document_registry,
    update_document,
)
from knowledge.normalized import NormalizedDocument
from knowledge.section import create_sections, get_section_text


"""Functions"""

def process_document(path: Path, source: str) -> NormalizedDocument:
    """Extracts and normalize a document into a NormalizedDocument #content_hash"""
    raw_content = extract_content(path)
    cleaned_content = normalize_whitespace(raw_content)
    
    return NormalizedDocument (
        document_id=None,
        source=source,
        modality=path.suffix.lstrip("."),
        sections=create_sections(cleaned_content)
    )
    
def extract_content(path: Path) -> str:
    """Responsible to get textual content from the source"""
    if path.suffix == ".pdf":
        return extract_pdf_text(path)
    elif path.suffix == ".txt":
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")


def check_document(path: Path, root: Path) -> str:
    """Returns the status of the document"""
    normalized_document = process_document(path, relative_source)
    relative_source = get_relative_source(path, root)
    received_hash = calculate_hash(normalized_document.content) #process_document(path)
    
    return get_processing_status(relative_source, received_hash)

def process_discovered_files(folder: Path, root: Path) -> None:
    """Process all discovered files in the given path, checking their status and updating the document_registry accordingly."""
    discovered_files = discover_files(folder)
    
    for file in discovered_files:
        relative_source = get_relative_source(file, root)
        normalized_document = process_document(file, relative_source)
        received_hash = calculate_hash(get_section_text(normalized_document.sections))
        print(f"{relative_source} -> "
              f"{received_hash}")
        
        doc_status = get_processing_status(relative_source, received_hash)
        
        if doc_status == "new":
            new_doc = create_document(relative_source, received_hash)
            register_document(new_doc)
            normalized_document.document_id = new_doc.document_id
            print(f"Registered new document: {new_doc}")
            
        elif doc_status == "changed":
            existing_doc = find_document(relative_source)
            
            if existing_doc:
                normalized_document.document_id = existing_doc.document_id
                update_document(existing_doc, received_hash)
                print(f"Updated existing document: {existing_doc}")
        
        else:
            print(f"No changes detected for document:: {relative_source}")
            


def run_ingestion(raw_folder: Path, manifest_path: Path) -> None:
    """Runs the ingestion pipeline by loading the registry, processing discovered files, and saving the updated registry"""
    load_document_registry(manifest_path)
    process_discovered_files(raw_folder, raw_folder)
    save_document_registry(manifest_path)