"""Imports"""
from dataclasses import dataclass 
import re

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


def is_section_heading(line: str) -> bool:
    return bool(re.match(r"^\d+\.\s+.+$", line))
        
# text = "Hello world"
# sections = create_sections(text)
# print(get_section_text(sections))
print(is_section_heading("1. Ginning"))
print(is_section_heading("2. Spinning"))
print(is_section_heading("10. Something"))
print(is_section_heading("The 1. process begins"))
print(is_section_heading("some normal paragraph"))