"""Imports"""
import re
import textwrap 
from knowledge.section import DocumentSection
from pathlib import Path

"""Functions"""
def create_slug(title: str) -> str:
    """Converts a title into a URL/filename-friendly slug."""
    new_title = re.sub(r"[^\w\d]+", "-", title)
    return new_title.lower().strip("-")

def create_okf_content(section: DocumentSection, source: str) -> str:
    #textwrap.dedent().strip() removes indentation
    return f"""---
type: Process
title: {section.title}
description: Traditional pre-weaving process in Bodo handloom preparation.
tags:
  - Bodo
  - handloom
  - weaving
  - cotton
status: draft
sources:
  - id: traditional-weaving-process
resource: ../../01_raw_data/{source}
title: Traditional Weaving Process of the Bodos
---
        
# {section.title}
        
{section.content}
""".strip()
    
    
def write_okf_file(content: str, output_path: Path) -> None:
    """Receives the OKF content and writes it to the output_path"""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
    
    except OSError as error:
        print(f"Failed to write OKF file {output_path}: {error}")
    
    
def generate_okf_concepts(sections: list[DocumentSection], source: str, output_dir: Path) -> None:
    for section in sections:
        if section.title is not None:
            title = create_slug(section.title)
            content = create_okf_content(section, source)
            output_path = output_dir / f"{title}.md"
            write_okf_file(content, output_path)

