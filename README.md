# LaTeX OCR with LLAMA Vision

Extract LaTeX code from images of mathematical equations using **Llama 3.2 Vision** — all running locally on your machine.

## Demo
- Test images are in the "test" folder
- Upload an image containing a math equation → get the raw LaTeX code + rendered equation instantly.

## Features

- Upload JPG/PNG images of math equations
- Extracts raw LaTeX code using Llama 3.2 Vision (via Ollama)
- Renders the extracted equation live in the browser
- Auto-fixes common LaTeX syntax issues (broken environments, unicode dashes, duplicate tags)
- Runs fully offline — no API keys needed

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI
- [Ollama](https://ollama.com/) — local LLM inference
- [Llama 3.2 Vision](https://ollama.com/library/llama3.2-vision) — vision model
- [Pillow](https://python-pillow.org/) — image handling

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running
- Llama 3.2 Vision model pulled

## Setup

1. Install Ollama and pull the model:
   ```bash
   ollama pull llama3.2-vision
   ```

2. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/mohdcodes/LaTex-OCR-with-llama-vision-model.git
   cd LaTex-OCR-with-llama-vision-model
   pip install streamlit ollama pillow
   ```

3. Run the app:
   ```bash
   streamlit run Latex-OCR-with-LLAMA/app.py
   ```

## Usage

1. Open the app in your browser (usually `http://localhost:8501`)
2. Upload an image of a math equation from the sidebar
3. Click **Extract LaTeX Code**
4. View the extracted LaTeX code and the rendered equation

---

Made by **MOHD ARBAAZ** — Data Science Engineer | [GitHub](https://github.com/mohdcodes) | [LinkedIn](https://www.linkedin.com/in/mohdcodes/)
