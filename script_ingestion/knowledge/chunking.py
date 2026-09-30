"""imports"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dataclasses import dataclass, field
from pathlib import Path
import yaml, uuid

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

"""functions"""
@dataclass
class Chunk:
    text: str
    source: str
    document_id: str
    chunk_index: int
    concept: str
    modality: str
    chunk_id: str 
    
def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0")
    elif overlap >= chunk_size:
        raise ValueError("Overlap must be less than chunk size")
    elif overlap < 0:
        raise ValueError("Overlap must be greater than or equal to 0")
    
    chunked = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunked.append(chunk)
        start += step
    return chunked

def create_chunks(text: str, chunk_size: int, overlap: int, source: str, document_id: str) -> list[Chunk]:
    chunked_texts = chunk_text(text, chunk_size, overlap)
    final_chunks = []
    for i, chunk in enumerate(chunked_texts):
        chunk_obj = Chunk(
            text=chunk,
            source=source,
            chunk_index=i,
            document_id=document_id
        )
        final_chunks.append(chunk_obj)
    return final_chunks

def split_with_langchain(text: str, chunk_size: int, chunk_overlap: int, source: str, document_id: str, concept: str, modality: str):
    """Creates chunks using langchain"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    res_chunks = []
    
    chunks = splitter.split_text(text)
    for i, chunk in enumerate(chunks):
        chunk_obj = Chunk(
            text=chunk,
            source=source,
            chunk_index=i,
            document_id=document_id,
            concept=concept,
            modality=modality,
            chunk_id=f"{document_id}_{i}",
        )
        res_chunks.append(chunk_obj)
    return res_chunks
    
def read_okf_file(path: Path) -> str:
    """Reads okf file from the okf directory"""
    content = path.read_text(encoding="utf-8")
    return content

def parse_okf_frontmatter(content: str) -> dict[str]:
    """Parses OKF frontmatter"""
    lines = content.splitlines()
    found_opening = False
    found_closing = False
    
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
                
    frontmatter_lines = lines[1: closing_index]
    res_frontmatter = "\n".join(frontmatter_lines)
        
    resultant_metadata = yaml.safe_load(res_frontmatter)
    return resultant_metadata
    
def parse_okf_body(content: str) -> str:
    """Parses OKF body"""
    lines = content.splitlines()
    found_opening = False
    found_closing = False
    
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
    
    body_lines = lines[closing_index + 1: ]
    res_body = "\n".join(body_lines).strip()
    
    return res_body
    
def process_okf_file(path: Path) -> list[Chunk]:
    """Processes one okf file"""
    content_file = read_okf_file(path)
    metadata = parse_okf_frontmatter(content_file)
    body = parse_okf_body(content_file)
    concept = metadata["title"]
    source = metadata["sources"][0]["resource"]
    modality = Path(metadata["sources"][0]["resource"]).suffix.lstrip(".")
    document_id = str(uuid.uuid4())
    chunk_size = 100
    chunk_overlap = 20
    chunks = split_with_langchain(
        body,
        chunk_size,
        chunk_overlap,
        source,
        document_id,
        concept,
        modality
    )

    return chunks


path = Path("knowledge_base/04_okf/processes/ginning.md")
# res = read_okf_file(path)
# metadata = parse_okf_frontmatter(res)
# body = parse_okf_body(res)
# print(metadata)
# print(body)
res_chunk = process_okf_file(path)
for i, chunk in enumerate(res_chunk):
    print(f"\nChunk Obj {i}: ")
    print(chunk)

# test1 = "abcdefghij"
# test2 = """
# Ginning is the first pre-weaving process of the Bodo traditional handloom.
# It involves separating cotton fibres from the seeds.
# The cleaned fibres are then prepared for the spinning process.
# """
# size = 4
# overlap = 2
# testing = split_with_langchain(test2, 100, 20)
# for index, chunk in enumerate(testing):
#     print(f"\nChunk {index}: ")
#     print(chunk)
# test_text = """
# Ginning is the first pre-weaving process of the Bodo traditional handloom.
# It involves separating cotton fibres from the seeds.
# The cleaned fibres are then prepared for the spinning process.
# """

# chunks = split_with_langchain(
#     text=test_text,
#     chunk_size=100,
#     chunk_overlap=20,
#     source="processes/Traditionalweaving_Process.pdf",
#     document_id="TEST_DOC_001",
#     concept="Ginning",
#     modality="pdf"
# )
# for i, chunk in enumerate(chunks):
#     print(f"\nChunk Obj {i}: ")
#     print(chunk)