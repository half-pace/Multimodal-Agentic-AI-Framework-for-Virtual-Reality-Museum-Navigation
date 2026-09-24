"""Imports"""
from dataclasses import dataclass

"""Dataclass structure"""
@dataclass
class DocumentSection:
    title: str | None
    content: str
    