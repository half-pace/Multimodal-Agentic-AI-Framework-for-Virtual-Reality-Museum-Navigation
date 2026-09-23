"""Imports"""
from dataclasses import dataclass


"""Represents normalized knowledge"""
@dataclass
class NormalizedDocument:
    document_id: str | None #stable indentity of the document - connects the normalized document back ot the document_registry. str | None because 
    source: str #where the original source came from
    modality: str #what type of source produced this content eg - pdf, text, img etc
    content: str # actual extracted textual representation