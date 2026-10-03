"""Testing ground to test the pipeline"""
"""Imports"""
from pathlib import Path
from ingestion.processing import run_ingestion, process_document, extract_content
from cleaning import normalize_whitespace
from knowledge.section import create_sections, DocumentSection
from knowledge.okf import (
    create_okf_content, 
    write_okf_file, 
    generate_okf_concepts, 
    generate_okf_index,
    validate_okf_file,
    validate_okf_bundle
)
from knowledge.document import (
    Document,
    calculate_hash,
    create_document,
)
from ingestion.manifest import (
    find_document,
    register_document,
    update_document,
    document_registry
)
from knowledge.chunking import (
    get_or_create_document,
    process_okf_file,
    process_okf_directory
)



# raw_folder = Path("knowledge_base/01_raw_data")
# manifest_path = Path("knowledge_base/document_manifest.json")

# run_ingestion(raw_folder, manifest_path)

#temporary
# path = Path("knowledge_base/01_raw_data/processes/Traditionalweaving_Process.pdf")

# raw_content = extract_content(path)
# cleaned_content = normalize_whitespace(raw_content)
# # for line in cleaned_content.splitlines()[:15]:
# #     print(repr(line))
# print("Extracted Characters: ", len(cleaned_content))

# sections = create_sections(cleaned_content)
# print("Number of sections: ", len(sections))

# # normalized_document = process_document(path, "processes/Traditionalweaving_Process.pdf")

# for section in sections:
#     print(section.title)
#     print(section.content[:200])
#     print("-" * 50)

# section = DocumentSection(
#     title="Ginning",
#     content="The ginning is the first pre weaving process..."
# )

# source = "processes/Traditionalweaving_Process.pdf"
# content = create_okf_content(section, source)

# output_path = Path("knowledge_base/04_okf/processes/ginning.md")

# write_okf_file(content, output_path)
# print(f"OKF file written to: {output_path}")

# path = Path("knowledge_base/01_raw_data/processes/Traditionalweaving_Process.pdf")
# path1 = Path("knowledge_base/04_okf/processes/ginning.md")

# source = "processes/Traditionalweaving_Process.pdf"

# raw_content = extract_content(path)
# cleaned_content = normalize_whitespace(raw_content)
# sections = create_sections(cleaned_content)
# output_dir = Path("knowledge_base/04_okf/processes")
# generate_okf_concepts(sections, source, output_dir)
# generated_files = list(output_dir.glob("*.md"))

# print("Number of OKF files:", len(generated_files))

# for file in generated_files:
#     print(file)

# generate_okf_index(output_dir)
# index_path = output_dir / "index.md"
# print("Index exists: ", index_path.exists())
# validation_res = validate_okf_file(path1)
# print("Validation is: ", validation_res)
# print(index_path.read_text(encoding="utf-8"))

# bundle_result = validate_okf_bundle(output_dir)
# print(f"Bundle validation: {bundle_result}")

# doc1 = get_or_create_document(
#     "processes/Traditionalweaving_Process.pdf",
#     "Ginning content"
# )

# print("Test 1:", doc1)


# doc2 = get_or_create_document(
#     "processes/Traditionalweaving_Process.pdf",
#     "Ginning content"
# )

# print("Test 2:", doc2)

# print("Same document ID:", doc1.document_id == doc2.document_id)
# print("Same version:", doc1.version == doc2.version)


# doc3 = get_or_create_document(
#     "processes/Traditionalweaving_Process.pdf",
#     "Ginning content changed"
# )

# print("Test 3:", doc3)

# print("Same document ID:", doc1.document_id == doc3.document_id)
# print("Version:", doc3.version)
# path = Path("knowledge_base/04_okf/processes/ginning.md")

# chunks = process_okf_file(path)

# for chunk in chunks:
#     print(chunk.document_id)
okf_directory = Path("knowledge_base/04_okf/processes")

all_chunks = process_okf_directory(okf_directory)

print("Total chunks:", len(all_chunks))

for chunk in all_chunks:
    print(chunk.concept, chunk.chunk_index, chunk.document_id)