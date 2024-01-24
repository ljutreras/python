import json
import openai
import os
from dotenv import load_dotenv
from v2.servicios.despedida import despedida
from servicios.detalle import detalle_de_la_deuda
from servicios.recibo import solicitar_recibo
from servicios.formas_y_lugares import formas_y_lugares_de_pago
import function_calling
from openai_repository import OpenAIChatClient
from function_callingv2 import ChatBot
from chat_message import ChatMessage

load_dotenv()

tools: list[dict] = [
                {
                    "type": "function",
                    "function": {
                        "name": "detalle_de_la_deuda",
                        "description": "proporciona un detalle de la deuda del usuario",
                        "parameters": {
                            "type": "object",
                            "properties": {},
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
                            "properties": {},
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
                            "properties": {},
                        }
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "despedida",
                        "description": "genera una respuesta fija como despedida la cual incluye el resumen de lo conversado",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                        }
                    },
                }
            ]
    
available_functions: dict[str: any] = {
    "detalle_de_la_deuda": detalle_de_la_deuda,
    "solicitar_recibo": solicitar_recibo,
    "formas_y_lugares_de_pago": formas_y_lugares_de_pago,
    "despedida": despedida
}

context: list[dict] = [ {'role':'system', 'content':"""
                        Eres un asistente virtual de Movistar, tu tarea principal es entregar informacion sobre el servicio telefonico. \
                        tienes 3 opciones disponibles, datalle de la deuda, formas y lugares de pago, solicitar un recibo. \

                        una vez recibido el mensaje del usuario debes retornar inmediatamente un mensaje \"necesito consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad DNI numerico del titular del servicio\"\
                        el documento de identidad del titular debe ser su DNI en formato de tipo numerico de maximo 9 caracteres y minimo 8 caracteres \
                        si el usuario ingresa otro mensaje, debes repetir de que ingrese el DNI del titular. \
                        cada vez que el usuario elija una opcion verifica si ya había proporcionado el DNI.\
                        si es así, no vuelvas a solicitarlo. \
                        de no ser una opcion valida, respondes lo delimitado por triple comillas invertidas 
                         ``` No puedo responder preguntas fuera del contexto telefonico``` \
                        no respondas preguntas que no tienen un contexto de pago de cuentas \
                        dale tiempo al usuario en caso de querer hacer una consulta a las otras opciones disponibles. \
                        Debes responder en un estilo amigable breve. \
                        debes mencionar que ingrese la palabra \"salir\" para finalizar la conversación.                        
"""
}]


# Mensaje de bienvenida
response: str = """
¡Hola! Bienvenid@ al chat de Movistar!
Estoy para ayudarte en:
🔹​Conocer detalle de tu deuda vencida
🔹​Formas y lugares de pago
🔹​Solicitar recibo
Comentanos, ¿qué necesitas?\n
"""
print(response)

while True:
    input_user: str = input('User: ')
    print(' ')
    if input_user.lower() == '':
        print(response)
    elif 'salir' not in input_user.lower():
        context.append({'role': 'user', 'content': input_user.lower()})
        context.append({'role':'assistant', 'content': 'necesito consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad DNI numerico del titular del servicio'})
        context.append({'role': 'user', 'content': input_user.lower()})
        response: str = ChatMessage(context, available_functions, tools)
        context.append({'role':'assistant', 'content': response.result})
        print(f'Assistant: {response.result} \n')
    else:
        break
