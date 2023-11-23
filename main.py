from pydantic import BaseModel
from fastapi import FastAPI
import requests
import openai
import json
import os

app = FastAPI()
openai.api_key=os.environ['API_KEY']

class User(BaseModel):
    message: str


app = FastAPI()

async def get_date_from_external_api():
        """get date from an external api"""

        api_url = "http://disal.mibot.cl/api2.php"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error al consumir la API externa. Código de estado: {response.status_code}"}


@app.post("/items/")
async def run_conversation(user: User):
        try:
            response = await get_date_from_external_api()
            # Step 1: send the conversation and available functions to the model
            messages=[
                {
                    'role': 'system',
                    'content':'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha'
                },
                {
                    'role':'user',
                    'content': f'{user}'
                }
            ]
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_date_from_external_api",
                        "description": "get date from an external api",
                        "parameters": { ## PARAMETROS SI NO ES UN POST
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "me puedes decir la fecha?",
                                },
                            },
                            "required": ["message"],
                        },
                    },
                }
            ]
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                tools=tools,
                tool_choice="auto",  # auto is default, but we'll be explicit
            )
            response_message = response.choices[0].message

            tool_calls = response_message.tool_calls
            # Step 2: check if the model wanted to call a function
            if tool_calls:
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                available_functions = {
                    "get_date_from_external_api": get_date_from_external_api,
                }
                messages.append(response_message)  # extend conversation with assistant's reply
                # Step 4: send the info for each function call and function response to the model
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(
                        message=function_args.get("message"),
                    )
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response
                second_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                )
                return second_response
        except TypeError as e:
            return e
