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
    current_title = None
    sections = []
    current_content = []
    
    for line in text.splitlines():
        if is_section_heading(line):
            title = re.sub(r"^\d+\.\s+", "", line)
            
            if current_title is not None:
                sections.append(
                    DocumentSection(
                        title=current_title,
                        content="\n".join(current_content).strip()
                    )
                )
            
            current_title = title
            current_content = []
        else:
            current_content.append(line)
            
    if current_title is not None:
        sections.append(
            DocumentSection(
                title=current_title,
                content="\n".join(current_content).strip()
            )
        )
    
    return sections

def get_section_text(sections: list[DocumentSection]) -> str:
    """Combines all section contents into 1 string"""
    return "\n".join(section.content for section in sections)


def is_section_heading(line: str) -> bool:
    return bool(re.match(r"^\d+\.\s+.+$", line))
        
text = """Traditional Weaving

1. Ginning
Ginning is the first process.
It's important

2. Spinning
Spinning prepares the yarn.

3. Reeling
Reeling is another process.
"""

sections = create_sections(text)

for section in sections:
    print(section)

