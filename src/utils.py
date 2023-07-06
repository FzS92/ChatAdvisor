"""
Utility functions for string manipulation and file operations.
"""

import re
from typing import List, Optional


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
    """Replaces a comma before a newline with a colon and space."""
    processed_lines = re.sub(r",\s*\n", ": ", input_text)
    return processed_lines


def string_to_list(string: str) -> List[str]:
    """Converts a comma-separated string into a list of words."""
    word_list = string.split(",")  # Split the string by comma
    word_list = [word.strip() for word in word_list]  # Remove leading/trailing spaces
    return word_list
