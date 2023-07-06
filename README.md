# Chat Advisor
This is a Python application that uses the OpenAI API to generate suggested answers for a given chat history. It takes input in the form of a chat history and user information, and provides two types of answers: a longer answer and a shorter answer.

The code for this project is also published on HuggingFace Space. You can access the web interface and try out the Chat Advisor by visiting the following link:

[HuggingFace Space: Chat Advisor](https://huggingface.co/spaces/fzs/ChatAdvisor)


## Installation

1. Clone the repository and go to the downloaded file:

```python
git clone https://github.com/FzS92/ChatAdvisor.git
```

2. Install the required dependencies:
```python
pip install -r requirements.txt
```
3. Obtain an OpenAI API key. You can sign up for an account and obtain the key from the OpenAI website.

## Usage
1. Run the application:
```python
python app.py
```

2. The application will launch a web interface where you can input the necessary information.

3. Provide the OpenAI API key, paste the chat history, enter your username, and specify the other usernames in the chat history (separated by commas).

4. Click the "Submit" button to generate the suggested answers.

5. The generated answers will be displayed in the web interface.

## Functionality
The application performs the following steps to generate the suggested answers:

1. Read the chat history.

2. Clean the chat history by removing square bracketed text and extra newlines.

3. Add the username at the end of the chat history.

4. Convert the other usernames into a list.

5. Make an API call to the OpenAI Completion model to generate a long answer based on the modified chat history.

6. Use the long answer as a prompt and make another API call to generate a shorter answer.

7. Display the modified chat history, the long answer, and the short answer in the web interface.

## File Structure
- **app.py**: The main Python script containing the application logic.
- **chat_history_sample.txt**: A sample chat history text file for preview purposes.
- **history_sample.txt**: A sample modified chat history text file for preview purposes.
- **README.md**: This README file.
## HuggingFace Space
The code for this project is also published on HuggingFace Space. You can access the web interface and try out the Chat Advisor by visiting the following link:

[HuggingFace Space: Chat Advisor](https://huggingface.co/spaces/fzs/ChatAdvisor)

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](https://rem.mit-license.org).

## Acknowledgments
The application uses the [OpenAI](https://openai.com/) API to generate suggested answers.
