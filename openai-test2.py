from fastapi import FastAPI
import requests
import openai
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI()

client = OpenAI()

class Message(BaseModel):
    message: str

def web_fecha():
    url = 'http://disal.mibot.cl/api2.php'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        data = respuesta.json()
        print("respuesta de la API WEB: ", data)
        fecha = data.get('fecha_actual', 'No disponible')
        return fecha
    else:
        return "Error al obtener la fecha"

def get_current_date():
    fecha_actual = web_fecha()
    return json.dumps({"fecha": fecha_actual})



    
@app.post("/consulta")
def comunicacionOpenAI(mensaje: Message):
    messages = [{"role": "system", "content": "Eres una agente virtual llamada Mia y tu objetivo es retornar la fecha actual."},{"role": "user", "content": mensaje.message}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Get the current date from a specific web page",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        }
    ]
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages= messages,
    tools=tools,
    tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls



    if tool_calls:

        available_functions = {
            "get_current_date": get_current_date,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_response = function_to_call(
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        ) 
        return second_response.choices[0].message

