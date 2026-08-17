# from pathlib import Path
# input_path = Path("knowledge_base/03_cleaned/materials/Raw Materials of Traditional Bodo Handloom.md")

# text = input_path.read_text(encoding="utf-8")

# for character in set(text):
#     if ord(character) < 32:
#         print(repr(character), ord(character))

sample = "Hello\r\nWorld\rTest\nAgain"

print("Before: ")
print(repr(sample))

sample = sample.replace("\r\n", "\n")
sample = sample.replace("\r", "\n")

print("After: ")
print(repr(sample))