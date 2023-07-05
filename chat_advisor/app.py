"""
Process chat history and generate suggested answers using the OpenAI API.
"""

import re
from typing import List, Tuple

import gradio as gr
import openai

chat_history_sample = """Son, [sunday 1:02pm]
Hey Mom, guess what? I scored the winning goal in today's soccer match!

Mother, [sunday 1:03pm]
Wow, that's amazing, sweetheart! I'm so proud of you. Tell me all about it!

Son, [sunday 1:09pm]
Well, it was a tough game, but in the last few minutes, I managed to dribble past the defenders and kick the ball right into the net. The crowd went wild!

Mother, [sunday 2pm]
That's incredible, my talented soccer star! You've been practicing so hard, and it's paying off. Keep up the great work!

Son, [sunday 2:00pm]
Thanks, Mom! It's all thanks to your support and encouragement. I couldn't have done it without you cheering me on from the sidelines.

Mother, [3:00]
You're welcome, my dear. It brings me joy to see you enjoying the sport and achieving your goals. Remember, teamwork and perseverance are key in any game, on and off the field.

Son, [another time]
I'll keep that in mind, Mom. And speaking of teamwork, we're planning a team outing next weekend to celebrate our victory. Can we go to the amusement park?
"""

history_sample = """Son: Hey Mom, guess what? I scored the winning goal in today's soccer match!
Mother: Wow, that's amazing, sweetheart! I'm so proud of you. Tell me all about it!
Son: Well, it was a tough game, but in the last few minutes, I managed to dribble past the defenders and kick the ball right into the net. The crowd went wild!
Mother: That's incredible, my talented soccer star! You've been practicing so hard, and it's paying off. Keep up the great work!
Son: Thanks, Mom! It's all thanks to your support and encouragement. I couldn't have done it without you cheering me on from the sidelines.
Mother: You're welcome, my dear. It brings me joy to see you enjoying the sport and achieving your goals. Remember, teamwork and perseverance are key in any game, on and off the field.
Son: I'll keep that in mind, Mom. And speaking of teamwork, we're planning a team outing next weekend to celebrate our victory. Can we go to the amusement park?
Mother:"""


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
    lines = input_text.split("\n")
    processed_lines = ""

    for line in lines:
        if line.endswith(","):
            line = line[:-1] + ": "
        elif line.endswith(", "):
            line = line[:-2] + ": "
        else:
            line = line + "\n"
        processed_lines += line
    return processed_lines


def string_to_list(string: str) -> List[str]:
    """Converts a comma-separated string into a list of words."""
    word_list = string.split(",")  # Split the string by comma
    word_list = [word.strip() for word in word_list]  # Remove leading/trailing spaces
    return word_list


# Inputs
openai_key = gr.Textbox(type="password", label="OpenAI Key")
chat_history = gr.Textbox(
    value=chat_history_sample, label="Paste your chat history here"
)
your_username = gr.Textbox(value="Mother", label="I need an answer for this username")
other_usernames = gr.Textbox(
    value="Son",
    label="What are the other usernames in the pasted chat history? Separate by comma.",
)

# outputs
previous_history = gr.Textbox(
    value=history_sample,
    label=(
        "We modify your chat history like this after you press submit (only for your"
        " reference!)."
    ),
)
longer_answer = gr.Textbox(value="Get your longer answer here", label="Long answer")
shorter_answer = gr.Textbox(
    value="Get your shorter answer here", label="Shorter answer"
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
