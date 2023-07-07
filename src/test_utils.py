"""
This module contains unit tests for the functions in the 'utils' module.
"""

from .utils import (
    add_name,
    read_string_from_file,
    remove_bracketed_text,
    remove_extra_newlines,
    replace_comma_before_newline,
    string_to_list,
)


def test_read_string_from_file(tmp_path):
    """
    Test the 'read_string_from_file' function.
    """
    file_content = "This is a test file."
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w", encoding="utf8") as file:
        file.write(file_content)

    result = read_string_from_file(file_path)
    assert result == file_content.strip()


def test_read_string_from_file_nonexistent_file(tmp_path):
    """
    Test the 'read_string_from_file' function with a nonexistent file.
    """
    file_path = tmp_path / "nonexistent_file.txt"

    result = read_string_from_file(file_path)
    assert result is None


def test_remove_bracketed_text():
    """
    Test the 'remove_bracketed_text' function.
    """
    history = "Hello [world], how are [you] doing?"
    cleaned_text = remove_bracketed_text(history)
    assert cleaned_text == "Hello , how are  doing?"


def test_remove_extra_newlines():
    """
    Test the 'remove_extra_newlines' function.
    """
    string = "Line 1\n\nLine 2\nLine 3\n\n\nLine 4"
    cleaned_string = remove_extra_newlines(string)
    assert cleaned_string == "Line 1\nLine 2\nLine 3\nLine 4"


def test_add_name():
    """
    Test the 'add_name' function.
    """
    string = "Hello"
    username = "John"
    result = add_name(string, username)
    assert result == "Hello\nJohn:"


def test_replace_comma_before_newline():
    """
    Test the 'replace_comma_before_newline' function.
    """
    input_text = "This is a test,\nThis is another test,\nAnd another test,\n"
    processed_lines = replace_comma_before_newline(input_text)
    expected_output = "This is a test: This is another test: And another test: "
    assert processed_lines == expected_output


def test_string_to_list():
    """
    Test the 'string_to_list' function.
    """
    string = "apple, banana, cherry, date"
    word_list = string_to_list(string)
    assert word_list == ["apple", "banana", "cherry", "date"]
