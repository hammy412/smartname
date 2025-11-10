import argparse
import requests
import pymupdf
from pathlib import Path
import base64
import json
import re

def main():
    parser = argparse.ArgumentParser(description="Rename files using Ollama's LLM.")
    parser.add_argument("directory", help="Path to the directory containing files to rename.")
    parser.add_argument("--execute", action="store_true", help="Execute the renaming of files.")
    parser.add_argument("--model", default="llama3.2-vision", help="Model to use for renaming files.")

    args = parser.parse_args()

    renamed = generate_filename_for_file(args)

    if args.execute:
        for old_path, new_name in renamed.items():
            new_path = old_path.with_name(new_name + old_path.suffix)
            old_path.rename(new_path)
            print(f"Renamed: {old_path} -> {new_path}")
    else:
        for old_path, new_name in renamed.items():
            print(f"Suggested: {old_path} -> {new_name + old_path.suffix}")


def generate_filename_for_file(args):
    directory = Path(args.directory)
    outputs = {}

    for file_path in directory.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower()

            if ext in ['.png', '.jpg']:
                with open(file_path, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read()).decode('utf-8')
                    outputs[file_path] = call_ollama_vision(image_data, args.model)
            elif ext in ['.txt', '.md', '.py']:
                with open(file_path, "r", encoding="utf-8") as text_file:
                    text = text_file.read()
                    outputs[file_path] = call_ollama_text(text, args.model)
    return outputs
                
def call_ollama_vision(image_data, model):
    prompt = "Analyze this file's content and suggest a concise, 3-5 word, descriptive filename. Use underscores instead of spaces. Do not include the file extension. Respond with *only* the filename and nothing else."
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "images": [image_data],
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 50
            }
        },
        timeout=30
    )

    # Parse multiple JSON objects line by line
    suggested = ""
    for line in response.text.strip().splitlines():
        try:
            chunk = json.loads(line)
            suggested += chunk.get("response", "")
        except json.JSONDecodeError:
            continue

    suggested = sanitize_filename(suggested.strip())
    if not suggested:
        suggested = "rename_me"

    print("Suggested filename:", suggested)
    return suggested

def call_ollama_text(text, model):
    prompt = "Analyze this file's content and suggest a concise, 3-5 word, descriptive filename. Use underscores instead of spaces. Do not include the file extension. Respond with *only* the filename and nothing else."
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt + "\n\n" + text[:2000],
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 50
            }
        },
        timeout=30
    )

    # Parse multiple JSON objects line by line
    suggested = ""
    for line in response.text.strip().splitlines():
        try:
            chunk = json.loads(line)
            suggested += chunk.get("response", "")
        except json.JSONDecodeError:
            continue

    suggested = suggested.strip()
    if not suggested:
        suggested = "rename_me"

    print("Suggested filename:", suggested)
    return suggested

def extract_pdf_image(): 
    pass

def extract_docx_content():
    pass

def extract_pptx_content():
    pass

def read_text_snippet():
    pass

def apply_casing():
    pass

def sanitize_filename(filename):
    # Remove illegal characters for filenames on most OS
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    
    # Remove surrounding whitespace
    filename = filename.strip()
    
    # Remove any file extension at the end (like .txt, .jpg, .pdf)
    filename = re.sub(r'\.[a-zA-Z0-9]{1,5}$', '', filename)
    
    # Replace spaces or multiple underscores with a single underscore
    filename = re.sub(r'[\s_]+', '_', filename)
    
    # Make sure it’s not empty
    if not filename:
        filename = "rename_me"
        
    return filename



if __name__ == "__main__":
    main()