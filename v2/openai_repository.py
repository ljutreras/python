import openai

class OpenAIChatClient:
    def __init__(self, api_key:str, messages, tools, model='gpt-3.5-turbo-1106', tool_choice="auto", temperature=0):
        
        openai.api_key = api_key
        self.messages = messages
        self.tools = tools
        self.model = model
        self.tool_choice = tool_choice
        self.temperature = temperature
        self.create_chat_completion()

    def create_chat_completion(self, ):
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice=self.tool_choice,
                temperature=self.temperature
            )
            self.result= response.choices[0].message
        except Exception as e:
            # Manejar errores de manera adecuada según tus necesidades
            print(f"Error al llamar a la API de OpenAI: {e}")
            self.result= None