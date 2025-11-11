# smartname

Smartname is a small AI-assisted command-line tool for renaming and organizing mixed-media files.

The tool analyzes file content (images, text, PDFs, Office documents) using a local LLM server and suggests concise descriptive filenames. It can run in dry-run mode (suggestions only) or rename files in-place.

Supported file types
- Images: .png, .jpg
- Text: .txt, .md, .py
- Documents: .pdf, .docx, .pptx

Key points
- PDF handling: the script extracts text from the first PDF page and uses the text-based LLM route. For scanned PDFs (no embedded text), consider rendering a page to an image and using the vision model or running OCR first.
- Filenames produced by the LLM are sanitized to remove illegal characters and collapse whitespace.

Requirements
- Python 3.8+
- Local Ollama server (or another compatible LLM endpoint)
- Python dependencies: listed below

Quick setup

1. Clone the repository

	git clone https://github.com/hammy412/smartname.git
	cd smartname

2. Create and activate a virtual environment

	python -m venv .venv
	# PowerShell (Windows)
	.\.venv\Scripts\Activate.ps1
	# CMD (Windows)
	.venv\Scripts\activate.bat
	# macOS / Linux
	source .venv/bin/activate

3. Install Python packages

	pip install pymupdf python-docx python-pptx requests

4. Run Ollama locally

Download and install Ollama from https://ollama.com then start the server locally:

	ollama serve

Pull the model you want to use (example):

	ollama pull llama3.2-vision

Usage

Show suggestions (dry-run):

	python .\rename_files.py C:\path\to\folder

Print and execute renames:

	python .\rename_files.py C:\path\to\folder --execute

Options
- --model: override the default model (default: llama3.2-vision)
- --execute: actually rename files; otherwise the script prints suggested names
- --case: provide the type of casing desired in the output file names (more info in CASING_GUIDE.md) (defaults to snake_case)