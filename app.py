import ollama
import json
import re

def get_user_input():
  
    user_input= input(("You:"))
    return user_input                               # user input 


def get_ai_response(messages, chunks):
    try:
        query = next(
            (
                item["content"]
                for item in reversed(messages)
                if item.get("role") == "user"
            ),
            ""
        )

        if query.lower().startswith("/doc "):
            doc_query = query[5:].strip()
            relevant_context = retrieve_relevant_chunks(
                doc_query, chunks
            )

            if not relevant_context:
                return "I couldn't find that information in the document."

            response = ollama.chat(
                model="gemma3:4b",
                messages=[
                    {
                        "role": "system",
                        # General-purpose system prompt for normal chat
                        "content": (
                        "You are a helpful general-purpose AI assistant. "
                        "Answer questions naturally and accurately. "
                        "Use the conversation history to understand the user. "
                        "Do not restrict answers to any document."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question: {doc_query}\n\n"
                            f"Document excerpts:\n{relevant_context}"
                        )
                    }
                ]
            )

            return response["message"]["content"]

        response = ollama.chat(
            model="gemma3:4b",
            messages=[
                {
                    "role": "system",
                    "content": (
                    "You are a helpful general-purpose AI assistant. "
                    "Answer naturally and helpfully using the conversation history."
                    )

                },
                *messages[-20:]
            ]
        )

        return response["message"]["content"]

   
    except Exception as e:
        # Log the error for debugging
        print(f"AI response error: {e}")

        # Return a user-friendly error message
        return (
            "Sorry, I couldn't get a response. "
            "Please check that Ollama is running "
            "and the gemma3:4b model is available."
        )

        # bot reply





def save_chat_history(messages):
    with open("chat_history.json", "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)         # save chat history



def load_document():
    with open("documents/notes.txt", "r", encoding="utf-8") as file:
        content = file.read()
    return content



def split_into_chunks(text, chunk_size=100):
    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)

    return chunks




def retrieve_relevant_chunks(query, chunks, top_k=2):
    stop_words = {
        "the", "a", "an", "is", "are", "what", "does",
        "do", "how", "about", "of", "in", "to", "and",
        "my", "me", "it", "this", "that", "document"
    }

    query_words = set(re.findall(r"\b[a-zA-Z0-9]+\b", query.lower()))
    query_words -= stop_words

    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(re.findall(r"\b[a-zA-Z0-9]+\b", chunk.lower()))
        score = len(query_words & chunk_words)

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)

    return "\n\n".join(
        chunk for score, chunk in scored_chunks[:top_k]
    )


def main():



    def load_chat_history():
        try:
            with open("chat_history.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []                      # load chat history

    
    messages = load_chat_history()


    document_text = load_document()
    chunks = split_into_chunks(document_text)



    while True:
        message = get_user_input()

        if message.lower() == "exit":
            print("Bot: Goodbye!")
            break

        messages.append({
            "role": "user",
            "content": message
            })

        op = get_ai_response(messages, chunks)
        print("Bot:", op)     

        messages.append({
        "role": "assistant",
        "content": op
            })    


        save_chat_history(messages)  

if __name__ == "__main__":
    main()          
    
    







