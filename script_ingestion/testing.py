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
from dataclasses import dataclass, field
import hashlib
# print(hashlib.sha256(b"Hello world").hexdigest())

text1 = "Castor is a food plant."
text2 = "Castor is a food plant."
text3 = "Castor is an important food plant."

@dataclass
class Document:
    document_id: str
    source: str
    content_hash: str
    version: int


def calculate_hash(input_string: str) -> str:
    hashlib_object = hashlib.sha256(input_string.encode("utf-8"))
    return hashlib_object.hexdigest()
    
document_obj = Document(
    document_id="DOC_001",
    source="test_source.md",
    content_hash=calculate_hash(text1),
    version=1
)

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