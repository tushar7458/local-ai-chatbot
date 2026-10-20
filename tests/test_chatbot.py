# Import the document chunking function
from app import split_into_chunks


# Test whether text is split into chunks correctly
def test_split_into_chunks():
    text = "abcdefghij"

    chunks = split_into_chunks(text, chunk_size=4)

    assert chunks == ["abcd", "efgh", "ij"]





# Import the document retrieval function
from app import retrieve_relevant_chunks


# Test whether relevant document text is retrieved
def test_retrieve_relevant_chunks():
    chunks = [
        "Python is a programming language.",
        "Ollama runs language models locally.",
        "The sky appears blue."
    ]

    result = retrieve_relevant_chunks(
        "What is Python?",
        chunks
    )

    assert "Python is a programming language." in result







# Test whether retrieval returns an empty result when nothing matches
def test_retrieve_no_matching_chunks():
    chunks = [
        "Python is a programming language.",
        "Ollama runs language models locally."
    ]

    result = retrieve_relevant_chunks(
        "What is the capital of Japan?",
        chunks
    )

    assert result == ""




# Import JSON and temporary-file utilities
import json


# Test whether conversation data can be saved and loaded
def test_chat_history_json_round_trip(tmp_path):
    chat_file = tmp_path / "chats.json"

    chats = {
        "chat-1": {
            "title": "Python Basics",
            "messages": [
                {"role": "user", "content": "What is Python?"},
                {"role": "assistant", "content": "Python is a programming language."}
            ]
        }
    }

    # Save the conversation data
    with open(chat_file, "w", encoding="utf-8") as file:
        json.dump(chats, file, indent=4, ensure_ascii=False)

    # Load the saved conversation data
    with open(chat_file, "r", encoding="utf-8") as file:
        loaded_chats = json.load(file)

    # Verify that the loaded data matches the original data
    assert loaded_chats == chats





# Import the JSON error type
import json


# Test how Python handles invalid JSON data
def test_invalid_json_raises_error(tmp_path):
    chat_file = tmp_path / "chats.json"

    # Write invalid JSON content to the file
    chat_file.write_text("{invalid json}", encoding="utf-8")

    # Verify that loading invalid JSON raises an error
    try:
        with open(chat_file, "r", encoding="utf-8") as file:
            json.load(file)
    except json.JSONDecodeError:
        error_raised = True
    else:
        error_raised = False

    assert error_raised is True

