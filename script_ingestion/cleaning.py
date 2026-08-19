from pathlib import Path

def normalize_whitespace(text: str) -> str:
    """ Cleans extracted texts by normalizing whitespaces """
    
    text = text.replace("\u00a0", " ")
    
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    
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

def validate_cleaned_text(text: str) -> bool:
    """ Validates the cleaned text - returns true when cleaned text contains usable content """
    
    return bool(text.strip())

def clean_file(input_path: Path, output_path: Path) -> None:
    """ Reads the texts from the input markdown file, cleans it, and saves it to the output path """
    try:
        
        text = input_path.read_text(encoding="utf-8")
    
        cleaned_text = normalize_whitespace(text)
    
        if not validate_cleaned_text(cleaned_text):
            print(f"Skipping empty file: {input_path}")
            return
    
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(cleaned_text, encoding="utf-8")
    except OSError as error: #OSERROR because it covers many filesystem-related problems
        print(f"Error processing file {input_path}: {error}")

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