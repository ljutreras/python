import json
from typing import Optional
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from prompt_general import prompt_general
from db.mysql_repository import connect_to_database
from servicios.detalle import detalle_de_la_deuda
from servicios.recibo import solicitar_recibo
from servicios.formas_y_lugares import formas_y_lugares_de_pago

load_dotenv()

connection = connect_to_database()
cursor = connection.cursor()

class User(BaseModel):
    id: Optional[str] = ''
    message: str

openai.api_key  = os.getenv('API_KEY')

def get_completion_from_messages(messages, temperature=0):
    tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "detalle_de_la_deuda",
                        "description": "obtiene el detalle de la deuda desde la base de datos mediante un prompt",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "se entregará una opcion valida del servicio detalle de la deuda",
                                },
                            },
                            "required": ["message"],
                        }
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "solicitar_recibo",
                        "description": "genera una respuesta generica la cual se le retorna al usuario",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "se entregará una opcion valida del servicio detalle de la deuda",
                                },
                            },
                            "required": ["message"],
                        }
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "formas_y_lugares_de_pago",
                        "description": "genera una respuestas la cual incluye las formas y lugares de pago",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "se entregará una opcion valida del servicio detalle de la deuda",
                                },
                            },
                            "required": ["message"],
                        }
                    },
                }
            ]
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "detalle_de_la_deuda": detalle_de_la_deuda,
            "solicitar_recibo": solicitar_recibo,
            "formas_y_lugares_de_pago": formas_y_lugares_de_pago
            }
        messages.append(response_message)
        
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
            )

        second_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0
        )
        print(function_name)
        return second_response.choices[0].message.content
    else:
        print('fuera del tools')
        return response_message.content


context = [ {'role':'system', 'content':"""
Eres chat de Movistar, un servicio que entrega la deuda del servicio telefonico de un usuario. \
una vez ingresado a una opcion debes retornar un mensaje \"necesito consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad DNI numerico del titular del servicio\"\
el documento de identidad del titular debe ser su DNI en formato de tipo numerico de maximo 9 caracteres y minimo 8 caracteres \
si el usuario ingresa otro mensaje, debes repetir de que ingrese el DNI del titular \
Espera para tener la solicitud completa por parte del usuario y comprueba si hay un final \
dale tiempo para saber si el cliente quiere añadir algo más. \
Asegúrese de aclarar todas las opciones \
Respondes en un estilo amigable breve y muy conversacional sin emojis. \
Para finalizar la conversación debes mencionarle que ingrese la palabra SALIR para terminar la conversacion. \
"""
}]

# def get_completion_from_messages_test(messages, model="gpt-3.5-turbo", temperature=0):
#     response = openai.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message.content

response = """
¡Hola! Bienvenid@ al chat de Movistar!
Estoy para ayudarte en:
🔹​Conocer detalle de tu deuda vencida
🔹​Formas y lugares de pago
🔹​Solicitar recibo
Comentanos, ¿qué necesitas?\n
"""

print(response)

while True:
    input_user = input('User: ')
    print(' ')
    if input_user.lower() == '' or 'hola' in input_user.lower():
        print(response)
    elif 'salir' not in input_user.lower():
        context.append({'role': 'user', 'content': input_user.lower()})
        response = get_completion_from_messages(context)
        context.append({'role':'assistant', 'content': response})
        print(f'Assistant: {response} \n')
    else:
        break
