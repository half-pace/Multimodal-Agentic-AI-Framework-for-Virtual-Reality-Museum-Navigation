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

#chunking testing
#we will use raise to raise and error deliberately - we will use ValueError

text = "abcdefghij"
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
    
try:
    chunk_text(text, chunk_size=0, overlap=0)
    #chunk_text(text, chunk_size=4, overlap=-1)
    #chunk_text(text, chunk_size=4, overlap=4)
    #chunk_text(text, chunk_size=4, overlap=5)
except ValueError as e:
    print(f"Error: {e}")    
#chunks = chunk_text(text, chunk_size=4, overlap=2)
#print(chunks)