"""Imports"""
import re
#import textwrap 
from knowledge.section import DocumentSection
from pathlib import Path

"""Functions"""
def create_slug(title: str) -> str:
    """Converts a title into a URL/filename-friendly slug."""
    new_title = re.sub(r"[^\w\d]+", "-", title)
    return new_title.lower().strip("-")

def create_okf_content(section: DocumentSection, source: str, document_id: str) -> str:
    #textwrap.dedent().strip() removes indentation
    return f"""---
type: Process
title: {section.title}
document_id: {document_id}
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
    
    
def generate_okf_concepts(sections: list[DocumentSection], source: str, document_id: str, output_dir: Path) -> None:
    for section in sections:
        if section.title is not None:
            title = create_slug(section.title)
            content = create_okf_content(section, source, document_id)
            output_path = output_dir / f"{title}.md"
            write_okf_file(content, output_path)

def generate_okf_index(output_dir: Path) -> None:
    """Find every .md file, ignore index.md if it exists already and rwites everything to index.md"""
    links = []
    output_path = output_dir / "index.md"
    for file in output_dir.rglob("*.md"):
        if file.name != "index.md":
            relative_path = file.relative_to(output_dir).as_posix()
            links.append(f"- [{file.stem.title()}]({relative_path})")
            
    content = "# Knowledge Bundle\n\n" + "\n".join(links)
    
    write_okf_file(content, output_path)
    

def validate_okf_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    found_opening = False
    found_closing = False
    required_fields = ["type:", "title:", "sources:"]
    
    if not lines or lines[0] != "---":
        return False
    
    for index, line in enumerate(lines):
        if line == "---":
            if found_opening:
                closing_index = index
                found_closing = True
                break
            found_opening = True
            
    if not found_closing:
        return False
    
    frontmatter_lines = lines[1 : closing_index]
    body_lines = lines[closing_index + 1 : ]
    
    for field in required_fields:
        if not any(line.startswith(field) for line in frontmatter_lines):
            return False
        
    if not any(line.strip() for line in body_lines):
        return False
    
    return True

def validate_okf_bundle(output_dir: Path) -> bool:
    all_valid = True
    
    for file in output_dir.rglob("*.md"):
        if file.name == "index.md":
            continue
        
        result = validate_okf_file(file)
        print(f"{file} : {result}")
        
        if not result:
            all_valid = False
        
    return all_valid