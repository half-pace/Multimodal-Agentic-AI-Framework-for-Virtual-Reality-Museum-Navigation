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

def get_section_text(sections: list[DocumentSection]) -> str:
    """Combines all section contents into 1 string"""
    return "\n".join(section.content for section in sections)
        
text = "Hello world"

sections = create_sections(text)
print(get_section_text(sections))