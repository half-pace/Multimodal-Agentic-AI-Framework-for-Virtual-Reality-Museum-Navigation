"""Testing ground to test the pipeline"""
"""Imports"""
from pathlib import Path
from ingestion.processing import run_ingestion, process_document, extract_content
from cleaning import normalize_whitespace
from knowledge.section import create_sections, DocumentSection
from knowledge.okf import create_okf_content, write_okf_file, generate_okf_concepts


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

path = Path("knowledge_base/01_raw_data/processes/Traditionalweaving_Process.pdf")

source = "processes/Traditionalweaving_Process.pdf"

raw_content = extract_content(path)
cleaned_content = normalize_whitespace(raw_content)
sections = create_sections(cleaned_content)
output_dir = Path("knowledge_base/04_okf/processes")
generate_okf_concepts(sections, source, output_dir)