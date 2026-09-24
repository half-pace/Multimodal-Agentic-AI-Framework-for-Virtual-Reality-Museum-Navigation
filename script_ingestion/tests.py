"""Testing ground to test the pipeline"""
"""Imports"""
from pathlib import Path
from ingestion.processing import run_ingestion, process_document, extract_content
from cleaning import normalize_whitespace
from knowledge.section import create_sections


raw_folder = Path("knowledge_base/01_raw_data")
manifest_path = Path("knowledge_base/document_manifest.json")

run_ingestion(raw_folder, manifest_path)

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