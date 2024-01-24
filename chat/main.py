import json
import openai
import os
from dotenv import load_dotenv
from despedida import despedida
from servicios.detalle import detalle_de_la_deuda
from servicios.recibo import solicitar_recibo
from servicios.formas_y_lugares import formas_y_lugares_de_pago

load_dotenv()

openai.api_key: str | None  = os.getenv('API_KEY')

def get_completion_from_messages(messages: str):
    """ conexion con openai mediante un historial de conversaciones y function callings

    Args:
        messages (str): el mensaje será proporcionado por el usuario el cual será derivado a las funciones si así lo infiere openai

    Returns:
        second_resonse (str) : respuesta de las diferentes funciones dentro de las function calling mencionadas en los tools
        response_message (str): respuesta si el mensaje no se encuentra dentro de las funciones proporcionadas en los tools
    """    

    tools: list[dict] = [
                {
                    "type": "function",
                    "function": {
                        "name": "detalle_de_la_deuda",
                        "description": "proporciona un detalle de la deuda del usuario",
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
                                    "description": "se entregará una opcion valida del servicio solicitar un recibo",
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
                                    "description": "se entregará una opcion valida del servicio de formas y lugares de pago",
                                },
                            },
                            "required": ["message"],
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
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "se entregará una despedida bajo un contexto de resumen",
                                },
                            },
                            "required": ["message"],
                        }
                    },
                }
            ]
    response: any = openai.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0,
    )
    response_message: any = response.choices[0].message
    tool_calls: list[any] | None = response_message.tool_calls

    if tool_calls:
        available_functions: dict[str: any] = {
            "detalle_de_la_deuda": detalle_de_la_deuda,
            "solicitar_recibo": solicitar_recibo,
            "formas_y_lugares_de_pago": formas_y_lugares_de_pago,
            "despedida": despedida
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

        second_response: any = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0
        )      
        return second_response.choices[0].message.content
    else:
        return response_message.content

context: list[dict] = [ {'role':'system', 'content':"""
                        Eres un asistente virtual de Movistar, tu tarea principal es entregar informacion sobre el servicio telefonico. \
                        tienes 3 opciones disponibles, datalle de la deuda, formas y lugares de pago, solicitar un recibo. \

                        una vez recibido el mensaje del usuario debes retornar un mensaje \"necesito consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad DNI numerico del titular del servicio\"\
                        el documento de identidad del titular debe ser su DNI en formato de tipo numerico de maximo 9 caracteres y minimo 8 caracteres \
                        si el usuario ingresa otro mensaje, debes repetir de que ingrese el DNI del titular. \
                        cada vez que el usuario elija una opcion verifica si ya había proporcionado el DNI.\
                        si es así, no vuelvas a solicitarlo. \
                        una vez retornado la respuesta de las funciones debes darle a conocer las opciones restantes. \
                        de no ser una opcion valida, debes mencionarle que se mantengan en el contexto del servicio telefonico volviendo a repetir las opciones validas \
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
        response: str = get_completion_from_messages(context)
        context.append({'role':'assistant', 'content': response})
        print(f'Assistant: {response} \n')
    else:
        break