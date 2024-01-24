class ChatBot:
    def __init__(self, available_functions=None):
        self.available_functions = available_functions or {}
        self.messages = []

    def process_tool_calls(self, response):
        res = self.messages[-1] if self.messages else None

        if response.tool_calls:
            self.available_functions
            self.messages.append(res)

            for tool_call in response.tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions.get(function_name)

                if function_to_call:
                    function_response = function_to_call()
                    self.messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
            return function_response
        else:
            return response.content