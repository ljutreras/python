""" 
OBJETIVOS DEL CHAT:
Las respuestas serán entregadas por ti , por lo que deberás idear un sistema que te permita entregar una respuesta predefinida .
Ninguna respuesta debe ser generada por ChatGPT.
"""

from openai import OpenAI
import json

client = OpenAI()

#Serie de funciones que seran agregadas a tools para ser llamadas por function calling de acuerdo a cada caso de uso requerido

def get_debt_detail():

    """Obtener el detalle de la deuda vencida

    Returns:
        json: Mensaje HardCoded que integra las variables "name","service","service_number","date","debt_amount" para retornar el detalle de la deuda del cliente
    """    

    name = "Ignacio"
    service = "movil"
    service_number = "12345"
    date = "08/07"
    debt_amount = str(100)

    return json.dumps({"nombre": f"{name} tienes un recibo pendiente de tu servicio {service} {service_number} que vencio el {date} por {debt_amount}. ¿Contamos con tu pago para hoy o mañana?"})

def get_payment_methods_and_locations():

    """Obtener las formas y lugares de pago

    Returns:
        json: Mensaje HardCoded que integra las variables "first_paragraph","second_paragraph", para retornar la informacion de las formas y lugares de pago
    """    

    first_paragraph = "En Movistar te brindamos diversas formas de pago SIN COMISIÓN.\nPuedes pagar por Yape: "
    second_paragraph = ", desde la web o app de tu banco.\nConoce todos los canales de pago en el siguiente link: "

    return json.dumps({"primer parrafo":first_paragraph,"pagina web para pagar": "https://innovacxion.page.link/mVFa","segundo parrafo":second_paragraph,"canal de pago":"https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago"})

def get_receipt():

    """Obtener el recibo

    Returns:
        json: Mensaje HardCoded que integra las variables "default_message","b2c" para retornar la información para de obtener el recibo
    """    
    default_message = "Obten tu recibo con solo unos clics: "
    b2c = "https://mirecibo.movistar.com.pe/"
    
    return json.dumps({"mensaje predeterminado":default_message,"url del recibo": b2c})

def get_goodbye():

    """Obtener despedida

    Returns:
        json: Mensaje que retorna una despedida al cliente cuando se siente satisfecho
    """    

    return json.dumps({"mensaje de despedida":"Gracias por elegir movistar, que tenga un buen dia :)"})

tools = [
        {
            "type": "function",
            "function": {
                "name": "get_debt_detail",
                "description": "Obtener el detalle de la deuda vencida",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_payment_methods_and_locations",
                "description": "Obtener las formas y lugares de pago",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_receipt",
                "description": "Obtener el recibo",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_goodbye",
                "description": "Reconocer si el usuario ya está satisfecho, no quiere seguir la conversación, no quiere seguir hablando o te agradece",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        }]

#Primer mensaje de rol system para indicar el comportamiento y logica que debera emplear la AI
messages = [{"role": "system", "content": "Eres un asistente virtual llamado chat Movistar, posees las siguientes funciones: get_debt_detail, get_payment_methods_and_locations, get_receipt, get_goodbye. Tu objetivo es determinar cual funcion utilizar para responderle al cliente, los temas que puedes responder para utilizar las funciones son: Detalle de la deuda, Solicitar recibo, Formas y lugares de pago."}]

#Mensaje inicial al ejecutar el codigo
print("\n        ¡Hola! Bienvendi@ al chat de Movistar!\n\nEstoy para ayudarte en:\n • Conocer detalle de tu deuda vencida\n • Formas y lugares de pago\n • Solicitar recibo\n\n        Comentanos,¿qué necesitas?\n")

client_input = input("Cliente: ").lower()

if client_input == "exit":
    exit()

if client_input:

    print("\n\nChat Movistar:\nNecesito que me des algunos datos para continuar con tu consulta.\nPor favor, ingresa el documento de identidad del titular del servicio.")
    
    for login_attempts in range(3):
            
            if client_input == "exit":
                break

            client_data_input = input("\nCliente: ").lower()

            if client_data_input == "exit":
                exit()

            #Aqui esta el documento de identidad que hay que ingresar para iniciar sesion y avanzar en el flujo de ejecución del codigo
            if client_data_input == "20252598":
                print("\n\nChat Movistar:\n\nBienvenido Ignacio\n\n")

                while client_input != "exit":

                    messages.append({"role":"user","content":client_input})

                    
                    response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages= messages,
                    tools=tools,
                    tool_choice="auto")

                    response_message = response.choices[0].message

                    tool_calls = response_message.tool_calls

                    if tool_calls:
                
                        available_functions = {
                        
                        "get_debt_detail": get_debt_detail,
                        "get_payment_methods_and_locations": get_payment_methods_and_locations,
                        "get_receipt": get_receipt,
                        "get_goodbye": get_goodbye
                        
                        }

                        messages.append(response_message)

                        for tool_call in tool_calls:
                            
                            function_name = tool_call.function.name
                            function_to_call = available_functions[function_name]
                            function_response = function_to_call(
                            )
                            messages.append({
                                
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response

                                })

                        movistar_chat_message = ""

                        function_response_dictionary = eval(function_response)
                        
                        for content in function_response_dictionary.values():
                            movistar_chat_message += str(content)

                        messages.append({"role":"assistant","content":movistar_chat_message})

                        print("\nChat Movistar:\n" + movistar_chat_message)

                        if movistar_chat_message == "Gracias por elegir movistar, que tenga un buen dia :)":
                            exit()

                        client_input = input("\nCliente: ").lower()

                    else:

                        topic_deviation_response = "Lo siento, Solo puedo responder a una de las 3 siguientes solicitudes:\n\n• Detalle de la deuda\n• Solicitar recibo\n• Formas y lugares de pago"

                        messages.append({"role":"assistant","content":topic_deviation_response})

                        print("\nChat Movistar:\n" + topic_deviation_response)

                        client_input = input("\nCliente: ").lower()

            else:

                print("\nChat Movistar:\nNo fue posible validar tu identidad.\nPor favor intenta nuevamente.")

    if client_data_input != "20252598":

        print("\nChat Movistar:\nDisculpa no puimos validar tu identidad.\nIntenta más tarde.\nQue tengas un buen dia.\n")