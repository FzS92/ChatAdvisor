"""
Chat Advisor

This script provides a chat advising functionality by utilizing OpenAI.
It allows users to input their chat history, OpenAI key, and usernames
to receive suggested answers.
The script utilizes the Gradio library for the user interface.
"""


import gradio as gr

from src import read_string_from_file, suggest_answer

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


if __name__ == "__main__":
    iface = gr.Interface(
        title="Chat Advisor",
        fn=suggest_answer,
        inputs=[openai_key, chat_history, your_username, other_usernames],
        outputs=[previous_history, longer_answer, shorter_answer],
    )
    iface.launch(share=False)  # share=True to share with others
