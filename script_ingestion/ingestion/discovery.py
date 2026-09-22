"""Imports"""
from pathlib import Path


"""Functions"""
def get_relative_source(file: Path, root: Path) -> str:
    """Returns the relative path of the file relative to our knowledge base - converts to POSIX-style path"""
    relative_path = file.relative_to(root)
    return relative_path.as_posix() 

def discover_files(folder: Path) -> list[Path]:
    discovered_files = []
    
    for file in folder.rglob("*"):
        if file.is_file():
            discovered_files.append(file)
    return discovered_files