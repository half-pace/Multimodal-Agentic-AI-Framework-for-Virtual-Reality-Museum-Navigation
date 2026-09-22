"""Imports"""
from dataclasses import dataclass

@dataclass
class NormalizedDocument:
    document_id: str #stable indentity of the document - connects the normalized document back ot the document_registry
    source: str #where the original source came from
    modality: str #what type of source produced this content eg - pdf, text, img etc
    content: str # actual extracted textual representation