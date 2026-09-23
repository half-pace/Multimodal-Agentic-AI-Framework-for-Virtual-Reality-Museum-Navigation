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


"""Functions"""

def process_document(path: Path) -> NormalizedDocument:
    """Extracts and normalize a document into a NormalizedDocument #content_hash"""
    if path.suffix == ".pdf":
        extracted_file = extract_pdf_text(path)
        cleaned_file = normalize_whitespace(extracted_file)
        normalized_document = NormalizedDocument(
            document_id="DOC102",
            source=path.as_posix(),
            modality="pdf",
            content=cleaned_file
        )
        return normalized_document #calculate_hash(cleaned_file)
    
    elif path.suffix == ".txt":
        cleaned_file = normalize_whitespace(
            path.read_text(encoding="utf-8")
        )
        normalized_document = NormalizedDocument(
            document_id="DOC101",
            source=path.as_posix(),
            modality="txt",
            content=cleaned_file
        )
        return normalized_document #calculate_hash(cleaned_file)
    
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    

def check_document(path: Path, root: Path) -> str:
    """Returns the status of the document"""
    normalized_document = process_document(path)
    relative_source = get_relative_source(path, root)
    received_hash = calculate_hash(normalized_document.content) #process_document(path)
    
    return get_processing_status(relative_source, received_hash)

def process_discovered_files(folder: Path, root: Path) -> None:
    """Process all discovered files in the given path, checking their status and updating the document_registry accordingly."""
    discovered_files = discover_files(folder)
    
    for file in discovered_files:
        normalized_document = process_document(file)
        relative_source = get_relative_source(file, root)
        received_hash = calculate_hash(normalized_document.content)
        
        doc_status = get_processing_status(relative_source, received_hash)
        
        if doc_status == "new":
            new_doc = create_document(relative_source, received_hash)
            register_document(new_doc)
            print(f"Registered new document: {new_doc}")
            
        elif doc_status == "changed":
            existing_doc = find_document(relative_source)
            
            if existing_doc:
                update_document(existing_doc, received_hash)
                print(f"Updated existing document: {existing_doc}")
        
        else:
            print(f"No changes detected for document:: {relative_source}")
            


def run_ingestion(raw_folder: Path, manifest_path: Path) -> None:
    """Runs the ingestion pipeline by loading the registry, processing discovered files, and saving the updated registry"""
    load_document_registry(manifest_path)
    process_discovered_files(raw_folder, raw_folder)
    save_document_registry(manifest_path)