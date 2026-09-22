"""Testing ground to test the pipeline"""
"""Imports"""
from pathlib import Path
from ingestion.processing import run_ingestion

raw_folder = Path("knowledge_base/01_raw_data")
manifest_path = Path("knowledge_base/document_manifest.json")

run_ingestion(raw_folder, manifest_path)