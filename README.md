
# Local AI Chatbot

A local AI chatbot built with Python, Streamlit, and Ollama. It runs a local language model and provides a browser-based chat interface with persistent conversation history.

## Features

- Chat with a locally running AI model.
- Browser-based interface built with Streamlit.
- Create and manage separate conversations.
- Rename, clear, and delete conversations.
- Save and restore conversations using JSON files.
- Ask questions about a local text document using document retrieval.
- Automated tests using pytest.

## Tech Stack

- Python
- Streamlit
- Ollama
- gemma3:4b
- JSON
- pytest

## Prerequisites

- Python installed on your computer.
- Ollama installed and running.
- The `gemma3:4b` model downloaded in Ollama.

## Setup

1. Clone or download this repository.
2. Open the project folder in your terminal.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Download the model if it is not already installed:

   ```bash
   ollama pull gemma3:4b
   ```

7. Start the Streamlit application:

   ```bash
   python -m streamlit run web_app.py
   ```

## Running Tests

Run the automated tests with:

```bash
python -m pytest -v
```

## Document Questions

The current document-question feature uses the text file at `documents/notes.txt`. Prefix a question with `/doc ` to ask about the document.

Example:

```text
/doc What does the document say about Python?
```

## Project Structure

```text
chatbot/
├── app.py
├── web_app.py
├── requirements.txt
├── README.md
├── documents/
│   └── notes.txt
└── tests/
    └── test_chatbot.py
```

Local chat history files are generated at runtime and should not be committed to the repository.

## Limitations

- The model runs locally, so response speed depends on your computer.
- Document retrieval currently uses simple keyword matching.
- The application requires Ollama and the selected model to be available locally.

## Future Improvements

- Improve background response handling while switching conversations.
- Add stronger error recovery and application-level tests.
- Improve document retrieval and support more file formats.
- Add further UI improvements and conversation management.

## License

Add a license before distributing this project publicly.
