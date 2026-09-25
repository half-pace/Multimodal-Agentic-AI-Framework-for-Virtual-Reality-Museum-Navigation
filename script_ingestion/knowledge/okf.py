"""Imports"""
import re
import textwrap 
from knowledge.section import DocumentSection

"""Functions"""
def create_slug(title: str) -> str:
    """Converts a title into a URL/filename-friendly slug."""
    new_title = re.sub(r"[^\w\d]+", "-", title)
    return new_title.lower().strip("-")

def create_okf_content(section: DocumentSection, source: str) -> str:
    return textwrap.dedent(f""" 
        ---
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
    """).strip()
    
    

    
    
    
