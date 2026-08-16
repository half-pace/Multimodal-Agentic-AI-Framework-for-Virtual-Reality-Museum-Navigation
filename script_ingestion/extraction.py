from pathlib import Path 
import pymupdf 

raw_folder = Path("knowledge_base/01_raw_data")
markdown_folder = Path("knowledge_base/02_markdown")

def run_extraction(raw_folder: Path, markdown_folder: Path) -> None:
    """ runs the extraction process for all pdfs in the raw data folder """
    
    for pdf in raw_folder.rglob("*.pdf"):
        relative = pdf.relative_to(raw_folder)
        inspect_pdf(pdf)
        markdown_text = extract_pdf_text(pdf)
        output = markdown_folder / relative.with_suffix(".md")
        save_markdown(markdown_text, output)
        
def inspect_pdf(pdf_path: Path) -> None:
    """ Opens a PDF document and displays basic info such as page count and metadata. """
    
    with pymupdf.open(pdf_path) as doc:
        metadata = doc.metadata or {} # {} - because some malformed pdfs may return None
        print(f"Number of pages: {len(doc)}")
        print(f"Metadata: {metadata}")
        

def extract_pdf_text(pdf_path: Path) -> str:
    with pymupdf.open(pdf_path) as doc:
        pages = []
        for page in doc:
            pages.append(page.get_text())
            
        markdown = "\n\n".join(pages)
    return markdown

def save_markdown(markdown_text: str, output_path: Path) -> None:
    """ Saves the extracted text as a markdown file """
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_text, encoding="utf-8")
    
    
if __name__ == "__main__":
    run_extraction(raw_folder, markdown_folder)