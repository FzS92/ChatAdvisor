"""
Process chat history and generate suggested answers using the OpenAI API.
"""

import re
from typing import List, Optional, Tuple

import gradio as gr
import openai


def read_string_from_file(file_path: str) -> Optional[str]:
    """
    Read the contents of a text file and return it as a string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str or None: The string read from the file, or None if an error occurred.
    """
    try:
        with open(file_path, "r", encoding="utf8") as file:
            string = file.read().strip()
        return string
    except IOError:
        print(f"Error: Failed to read the file '{file_path}'.")
        return None


def remove_bracketed_text(history: str) -> str:
    """Removes text enclosed in square brackets from the chat history."""
    cleaned_text = re.sub(r"\[.*?\]", "", history)
    return cleaned_text


def remove_extra_newlines(string: str) -> str:
    """Removes extra newlines from a string."""
    return "\n".join(line for line in string.splitlines() if line.strip())


def add_name(string: str, username: str) -> str:
    """Adds the given username at the end of the string."""
    return string + username + ":"


def replace_comma_before_newline(input_text: str) -> str:
    """Replaces a comma before a newline with a colon."""
    processed_lines = re.sub(r",\n|, \n", ": ", input_text)
    return processed_lines


def string_to_list(string: str) -> List[str]:
    """Converts a comma-separated string into a list of words."""
    word_list = string.split(",")  # Split the string by comma
    word_list = [word.strip() for word in word_list]  # Remove leading/trailing spaces
    return word_list


# Inputs
chat_history_sample = read_string_from_file("./example/chat_history_sample.txt")

openai_key = gr.Textbox(
    label="OpenAI Key", placeholder="Enter your OpenAI key", type="password"
)
chat_history = gr.Textbox(
    placeholder=chat_history_sample, label="Paste your chat history here"
)
your_username = gr.Textbox(
    placeholder="Mother", label="I need an answer for this username"
)
other_usernames = gr.Textbox(
    placeholder="Son",
    label="What are the other usernames in the pasted chat history? Separate by comma.",
)

# outputs
history_sample = read_string_from_file("./example/history_sample.txt")

previous_history = gr.Textbox(
    placeholder=history_sample,
    label=(
        "We modify your chat history like this after you press submit (only for your"
        " reference!)."
    ),
)
longer_answer = gr.Textbox(
    placeholder="Get your longer answer here", label="Long answer"
)
shorter_answer = gr.Textbox(
    placeholder="Get your shorter answer here", label="Shorter answer"
)


def suggest_answer(
    openaikey: str, history: str, your_usern: str, other_usern: str
) -> Tuple[str, str, str]:
    """Generates a suggested answer based on the given chat history
    and user information using the OpenAI API."""
    openai.api_key = openaikey
    updated_history = history
    updated_history = remove_extra_newlines(updated_history)
    updated_history = remove_bracketed_text(updated_history)
    updated_history = replace_comma_before_newline(updated_history)
    updated_history = add_name(updated_history, your_usern)
    other_usern = string_to_list(other_usern)

    updated_history = str(updated_history)
    other_usernames = str(other_usern)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=updated_history,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=other_usernames,
    )

    long_answer = response["choices"][0]["text"]

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{long_answer}\n\nTl;dr",
        temperature=1,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1,
    )

    short_answer = response["choices"][0]["text"]
    return updated_history, long_answer, short_answer


if __name__ == "__main__":
    iface = gr.Interface(
        title="Chat Advisor",
        fn=suggest_answer,
        inputs=[openai_key, chat_history, your_username, other_usernames],
        outputs=[previous_history, longer_answer, shorter_answer],
    )
    iface.launch(share=False)
