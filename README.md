# Streamlit Chatbot Interface

This project demonstrates a simple chatbot interface using Streamlit and the OpenAI GPT-3.5-turbo model. Users can interact with the chatbot by entering messages, and the chatbot responds based on the conversation history.

## Dependencies
- [OpenAI](https://beta.openai.com/signup/): The OpenAI API is used for natural language processing and generating chatbot responses.
- [Streamlit](https://streamlit.io/): Streamlit is used to create a user-friendly web interface for the chatbot.
- [dotenv](https://pypi.org/project/python-dotenv/): The dotenv library is used for loading environment variables.

## Functionality
1. The chat history is stored using the `shelve` library to persist messages across interactions.
2. Users can delete the chat history by clicking the "Delete Chat History" button in the sidebar.
3. Messages are displayed with avatars indicating whether they are from the user or the chatbot.
4. Users input messages in the chat input box, and the conversation history is updated accordingly.
5. The OpenAI GPT-3.5-turbo model is used to generate responses based on the user's input and the existing conversation history.

## Implementation
- The chat history is initialized or loaded from a shelve file at the beginning of each session.
- Streamlit's `st.chat_message` and `st.chat_input` are utilized for displaying messages and capturing user input.
- The OpenAI GPT-3.5-turbo model is accessed through the OpenAI API, and the generated responses are displayed in the chat.

## Usage
1. Run the Streamlit app with `streamlit run <filename>.py`.
2. Interact with the chatbot by entering messages in the chat input box.
3. Optionally, delete the chat history by clicking the "Delete Chat History" button.

Note: Ensure that you have the required API key from OpenAI and necessary dependencies installed.

## Code Structure
- The code is organized into functions for loading and saving chat history, initializing the OpenAI model, and handling the main chat interface.
- The Streamlit app's layout includes a sidebar for additional functionality.

