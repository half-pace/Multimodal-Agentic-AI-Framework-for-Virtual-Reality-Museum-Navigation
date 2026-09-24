"""Imports"""
from dataclasses import dataclass 

"""Dataclass structure"""
@dataclass
class DocumentSection:
    title: str | None
    content: str

def create_sections(text: str) -> list[DocumentSection]:
    """Creates sections from cleaned texts"""
    
    return [DocumentSection(
        title=None,
        content=text
    )]

text = "Traditional weaving begins with preparation of the yarn."

sections = create_sections(text)
print(sections)