from typing import Optional
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from db.mysql_repository import connect_to_database
from db.insert_db import insert_db
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

def chat_movistar():
    try:
        context = [ {'role':'system', 'content':"""
                            Bienveni@ al chat de Movistar, un servicio que entregar la deuda del servicio telefonico de un usuario. \
                            Primero saludas al cliente \
                            luego le dices tus servicios y en que puedes ayudarlo, \
                            luego pregunta si necesita ayuda con los conocer detalle de la deuda, formas y lugares de pago o solicitar recibo. \
                            cuando el usuario responda le mencionas que necesitas consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad del titular del servicio\
                            Espera para tener la solicitud completa y comprueba si hay un final \
                            dale tiempo para saber si el cliente quiere añadir algo más. \
                            Asegúrese de aclarar todas las opciones \
                            identificar el elemento del menú.\
                            Respondes en un estilo amigable breve y muy conversacional. \
                            Para finalizar la conversación debes mencionarle que ingrese la palabra SALIR para terminar la conversacion. \
                            """
                        } ]
        tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "detalle_de_la_deuda",
                        "description": "obtiene el detalle de la deuda desde la base de datos",
                        "parameters": {
                            "type": "object",
                            "properties": {}
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
                            "properties": {}
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
                            "properties": {}
                        }
                    },
                }

            ]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=context,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )
            
        response_content = response.choices[0].message.content if response.choices else ""
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            available_functions = {
                "detalle_de_la_deuda": detalle_de_la_deuda,
                "solicitar_recibo": solicitar_recibo,
                "formas_y_lugares_de_pago": formas_y_lugares_de_pago,
                }
            context.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_response = function_to_call()
                context.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            second_response = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                context=context,
                temperature=0
            )
            print(context)
            print(f'Assistant: {second_response.choices[0].message.content}')
        else:
            print(context)
            print(f'Assistant: {response_content}')

    except:
        pass


context = [ {'role':'system', 'content':"""
Eres chat de Movistar, un servicio que entregar la deuda del servicio telefonico de un usuario. \
Primero saludas al cliente con un bienvenido al chat de movistar. \
luego pregunta si necesita ayuda con los conocer detalle de la deuda, formas y lugares de pago o solicitar recibo. \
cuando el usuario responda le mencionas que necesitas consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad del titular del servicio\
Espera para tener la solicitud completa y comprueba si hay un final \
dale tiempo para saber si el cliente quiere añadir algo más. \
Asegúrese de aclarar todas las opciones \
identificar el elemento del menú.\
Respondes en un estilo amigable breve y muy conversacional. \
Para finalizar la conversación debes mencionarle que ingrese la palabra SALIR para terminar la conversacion. \
"""
} ]



def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content


while True:
    input_user = input('User: ')
    if 'salir' not in input_user.lower():
        context.append({'role': 'user', 'content': input_user})
        response = get_completion_from_messages(context)
        context.append({'role':'assistant', 'content': response})
        print(f'Assistant: {response}')
    else:
        break


