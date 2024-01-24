import os
from openai_repository import OpenAIChatClient
from function_callingv2 import ChatBot


class ChatMessage:
    def __init__(self, message, available_functions, tools):
        self.message = message
        self.available_functions = available_functions
        self.tools = tools
        self.chat_completions_from_message()  # Llamada al método al instanciar la clase


    def chat_completions_from_message(self):
        response: any = OpenAIChatClient(os.getenv("API_KEY"),self.message, self.tools)

        chat_bot = ChatBot(self.available_functions)
        self.result = chat_bot.process_tool_calls(response.result)
