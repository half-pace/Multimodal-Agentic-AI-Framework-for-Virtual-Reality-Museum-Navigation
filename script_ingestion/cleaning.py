from pathlib import Path

def normalize_whitespace(text: str) -> str:
    """ Cleans extracted texts by normalizing whitespaces """
    
    text = text.replace("\u00a0", " ")
    lines = text.splitlines()
    
    cleaned_lines = []
    previous_blank = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
            continue
        
        cleaned_lines.append(line)
        previous_blank = False
            
    return "\n".join(cleaned_lines).strip()

def clean_file(input_path: Path, output_path: Path) -> None:
    """ Reads the texts from the input markdown file, cleans it, and saves it to the output path """
    
    text = input_path.read_text(encoding="utf-8")
    
    cleaned_text = normalize_whitespace(text)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(cleaned_text, encoding="utf-8")
    
def run_cleaning(input_folder: Path, output_folder: Path) -> None:
    """ Runs the cleaning function / finds and processes all files """
    
    for markdown_file in input_folder.rglob("*.md"):
        relative = markdown_file.relative_to(input_folder)
        
        output_path = output_folder / relative
        clean_file(markdown_file, output_path)


if __name__ == "__main__":
    input_folder = Path("knowledge_base/02_markdown")
    output_folder = Path("knowledge_base/03_cleaned")

    run_cleaning(input_folder, output_folder)