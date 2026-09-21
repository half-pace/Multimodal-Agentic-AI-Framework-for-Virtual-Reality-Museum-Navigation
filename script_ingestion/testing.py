# from pathlib import Path
# input_path = Path("knowledge_base/03_cleaned/materials/Raw Materials of Traditional Bodo Handloom.md")

# text = input_path.read_text(encoding="utf-8")

# for character in set(text):
#     if ord(character) < 32:
#         print(repr(character), ord(character))

# sample = "Hello\r\nWorld\rTest\nAgain"

# print("Before: ")
# print(repr(sample))

# sample = sample.replace("\r\n", "\n")
# sample = sample.replace("\r", "\n")

# print("After: ")
# print(repr(sample))

# def validate_cleaned_text(text: str) -> bool:
#     return bool(text.strip())


# print(validate_cleaned_text("Hello world"))
# print(validate_cleaned_text(""))
# print(validate_cleaned_text("     "))
# print(validate_cleaned_text("\n\n"))
# print(validate_cleaned_text("Castor\nRicinus communis"))

#chunking testing 1
#we will use raise to raise and error deliberately - we will use ValueError

# text = "abcdefghij"
# def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
#     if chunk_size <= 0:
#         raise ValueError("Chunk size must be greater than 0")
#     elif overlap >= chunk_size:
#         raise ValueError("Overlap must be less than chunk size")
#     elif overlap < 0:
#         raise ValueError("Overlap must be greater than or equal to 0")

#     chunked = []
#     start = 0
#     step = chunk_size - overlap
#     while start < len(text):
#         chunk = text[start:start + chunk_size]
#         chunked.append(chunk)
#         start += step
#     return chunked
    
# try:
#     chunks = chunk_text(text, chunk_size=4, overlap=2)
#     print(chunks)
#     #chunk_text(text, chunk_size=4, overlap=-1)
#     #chunk_text(text, chunk_size=4, overlap=4)
#     #chunk_text(text, chunk_size=4, overlap=5)
# except ValueError as e:
#     print(f"Error: {e}")    
#chunks = chunk_text(text, chunk_size=4, overlap=2)
#print(chunks)

#using dataclass for chunking - testing 2
# from dataclasses import dataclass, field
# import random

# def generate_id():
#     id = random.randint(0, 5)
#     return id

# @dataclass
# class Chunk:
#     text: str
#     source: str 
#     chunk_id: str = field(default_factory=generate_id)
    
# chunk1 = Chunk(
#     text = "Castor is a food plant.",
#     source = "foodplants.md"
# )

# chunk2 = Chunk(
#     text = "Kesseru is another food plant.",
#     source = "foodplants.md"
# )

# print(chunk1)
# print(chunk2)
# print(chunk1.chunk_id == chunk2.chunk_id)
#This should print False since each chunk should have a unique ID

#testing 3
# from dataclasses import dataclass, field
# import random
# import hashlib

# text = "abcdefghij"

# def generate_id():
#     chunk_id_gen = random.randint(0, 5)
#     return chunk_id_gen
# @dataclass
# class Chunk:
#     text: str
#     source: str
#     document_id: str
#     chunk_index: int
#     chunk_id: str = field(default_factory=generate_id)

# @dataclass
# class Document:
#     document_id: str
#     source: str
#     content_hashing: str
    
# def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
#     if chunk_size <= 0:
#         raise ValueError("Chunk size must be greater than 0")
#     elif overlap >= chunk_size:
#         raise ValueError("Overlap must be less than chunk size")
#     elif overlap < 0:
#         raise ValueError("Overlap must be greater than or equal to 0")

#     chunked = []
#     start = 0
#     step = chunk_size - overlap
#     while start < len(text):
#         chunk = text[start:start + chunk_size]
#         chunked.append(chunk)
#         start += step
#     return chunked

# def create_chunks(text: str, chunk_size: int, overlap: int, source: str, document_id: str) -> list[Chunk]:
#     chunked_texts = chunk_text(text, chunk_size, overlap)
#     final_chunks = []
#     for i, chunk in enumerate(chunked_texts):
#         chunk = Chunk(
#             text=chunk,
#             source=source,
#             chunk_index=i,
#             document_id = document_id
#         )
#         final_chunks.append(chunk)
#     return final_chunks

# try:
#     chunks = create_chunks(text, chunk_size=4, overlap=2, source="test_source.md", document_id="DOC_001")
#     for chunk in chunks:
#         print(chunk)
#     print(chunks)
        
# except ValueError as e:
#     print(f"Error: {e}")

#testing 4
from dataclasses import dataclass
from pathlib import Path
import hashlib, uuid, json
from extraction import *
from cleaning import *

# print(hashlib.sha256(b"Hello world").hexdigest())

text1 = "Castor is a food plant."
text2 = "Castor is a food plant."
text3 = "Castor is an important food plant."

document_registry = {}

@dataclass
class Document:
    document_id: str
    source: str
    content_hash: str
    version: int

def generate_document_id() -> str:
    return str(uuid.uuid4())

def calculate_hash(input_string: str) -> str:
    hashlib_object = hashlib.sha256(input_string.encode("utf-8"))
    return hashlib_object.hexdigest()
    
document_obj = Document(
    document_id=generate_document_id(),
    source="castor.pdf",
    content_hash=calculate_hash(text1), #text1
    version=1
)
document_obj1 = Document(
    document_id=generate_document_id(),
    source="processes/Traditionalweaving_Process.pdf",
    content_hash=calculate_hash(text2), #text2
    version=1
)

document_registry.update({document_obj.source: document_obj, document_obj1.source: document_obj1})

def find_document(source: str) -> Document | None: #search document_registry using source and return corresponding Document
    for document in document_registry.keys():
        if source == document:
            print(f"Document found: {document_registry[document]}")
            return document_registry[document]
    
    return None

def has_content_changed(existing_hash: str, new_hash: str) -> bool:
    if existing_hash == new_hash:
        #print("Content has not changed.")
        return False
    else:
        #print("Content has changed.")
        return True

old_hash = calculate_hash(text1)
new_hash_same = calculate_hash(text2)
new_hash_changed = calculate_hash(text3)

print(has_content_changed(old_hash, new_hash_same))  # Should print "Content has not changed." and return False
print(has_content_changed(old_hash, new_hash_changed))  # Should print "Content has changed." and return True

def update_document(document: Document, changed: bool, new_hash: str) -> None:
    if changed:
        document.version += 1
        document.content_hash = new_hash
        print(f"Document updated to version {document.version}.")
    else:
        print("No update needed; content has not changed.")

print(calculate_hash(text1))
print(document_obj)
update_document(document_obj, has_content_changed(old_hash, new_hash_same), new_hash_same)
update_document(document_obj, has_content_changed(old_hash, new_hash_changed), new_hash_changed)
print(document_obj)

print(document_obj1)
print(document_registry)
print(find_document("castor.pdf"))
print(find_document("eri.pdf"))

#testing 5 - file discovery 
# from pathlib import Path
# import json

root = Path("knowledge_base/01_raw_data")
file = Path("knowledge_base/01_raw_data/processes/Traditionalweaving_Process.pdf")

def get_relative_source(file: Path, root: Path): #answers - Where is this file relative to our knowledge-base root?
    relative_path = file.relative_to(root)
    return relative_path.as_posix()  # Convert to POSIX-style path (with forward slashes)


def discover_files(folder: Path):
    discovered_files = []
    for file in folder.rglob("*"):
        if file.is_file():
            print(file)
            discovered_files.append(file)
    return discovered_files

def is_document_registered(source: str) -> bool:
    return source in document_registry

def get_document_status(source: str) -> str:
    return "existing" if source in document_registry else "new"

def get_processing_status(source: str, new_hash: str) -> str:
    if is_document_registered(source):
        existing_document = find_document(source)
        if existing_document:
            if has_content_changed(existing_document.content_hash, new_hash):
                return "changed"
            else:
                return "unchanged"
    return "new"

def save_document_registry(path: Path) -> None:
    data = {}
    
    for source, document in document_registry.items(): #convert document object into a dictionary too
        document_data = {
            "document_id": document.document_id,
            "source": document.source,
            "content_hash": document.content_hash,
            "version": document.version
        }
        
        data[source] = document_data
    
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
def load_document_registry(path: Path) -> None: #reverse of save_document_registry - load the document registry from a JSON file
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for source, document_data in data.items():
                document_obj = Document(
                    document_id=document_data["document_id"],
                    source=document_data["source"],
                    content_hash=document_data["content_hash"],
                    version=document_data["version"]
                )
                document_registry[source] = document_obj
                            
#pipeline process 
def process_document(path: Path) -> str:
    
    extracted_file = extract_pdf_text(path)
    cleaned_file = normalize_whitespace(extracted_file)
    content_hash = calculate_hash(cleaned_file)
    return content_hash

def check_document(path: Path, root: Path) -> str:
    relative_source = get_relative_source(path, root)
    received_hash = process_document(path)
    doc_status = get_processing_status(relative_source, received_hash)
    
    return doc_status

def create_document(source: str, content_hash: str) -> Document:
    document_obj = Document(
        document_id=generate_document_id(),
        source=source,
        content_hash=content_hash,
        version=1
    )
    #document_registry[source] = document_obj
    return document_obj    

def register_document(document: Document) -> None:
    """Update the document registry with the given document. If the document already exists, update its version and hash."""
    document_registry[document.source] = document


files = discover_files(root)
print(files)
print(get_relative_source(file, root))
print(is_document_registered("processes/Traditionalweaving_Process.pdf"))
print(is_document_registered("processes/Traditionalweaving_Process1.pdf"))
print(get_document_status("processes/Traditionalweaving_Process.pdf"))
print(get_document_status("processes/Traditionalweaving_Process1.pdf"))
print(get_processing_status("processes/Traditionalweaving_Process.pdf", new_hash_changed))
print(get_processing_status("processes/Traditionalweaving_Process.pdf", new_hash_same))
print(get_processing_status("processes/Traditionalweaving_Process1.pdf", new_hash_same))
save_document_registry(Path("knowledge_base/document_manifest.json"))

document_registry.clear()  # Clear the current registry to simulate a fresh start
print(document_registry)

load_document_registry(Path("knowledge_base/document_manifest.json"))
print(document_registry)
test_doc_process = Path("knowledge_base/01_raw_data/processes/Traditionalweaving_Process.pdf")
print(process_document(test_doc_process))  # This will extract, clean, and hash the content of the PDF
load_document_registry(Path("knowledge_base/document_manifest.json"))
print(document_registry)
print(check_document(test_doc_process, root))

new_doc = create_document(
    "materials/example1.pdf",
    "as1kj2kb4kqj2b3"
)
print(new_doc)
