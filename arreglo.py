from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict
import os


load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.environ['API_KEY'])

class User(BaseModel):
    user_message: str

historial_conversacion = []
""" Simula el comportamiento de una base de datos, captando el mensaje que responde la IA para así realizar las validaciones 
    como si el usuario existiera en la base de datos"""

def esSaludo(mensaje_usuario: str) -> bool:
    """ Detecta el saludos, para inicar la conversacion """

    saludos = ["hola", "buenos días", "buenas tardes", "buenas noches", "saludos"]
    mensaje_usuario = mensaje_usuario.lower()
    return any(saludo in mensaje_usuario for saludo in saludos)

def nombre():
    """ Darle más identidad al chat """
    return "Me llamo REL y soy un asistente de Movistar, encantado de conocerte. ¿Eres cliente de Movistar?"

def esMovistar():
    """ Esto en el caso de que si el usuario se desvía y aclara que si es usuario de Movistar """
    return "Perfecto, por favor introduzca su numero de identificacion"

def bienvenida() -> str:
    """ Saluda con un mensaje predeterminado """

    return "Hola, soy un agente de Movistar. ¿Me puedes dar tu identificación de id? para Validar con la Base de datos. Por favor escriba solo el numero de ID"

def validarCliente(identificacion: str) -> str:
    """ Realiza una simulacion con consultar a la base de datos si existe el usuario o no, solo valida 6 digitos,
    se cierra cuando el usuario se equivoca mas de dos veces.
    Solo recibe digitos para realizar la validaciones ejemplo: 123456= que sería valido o 1234 = sería no válido """

    numeros_identificacion = ''.join(filter(str.isdigit, identificacion))
    intentos_fallidos = sum(1 for msg in historial_conversacion if "inválido" in msg.get("content", ""))
    if len(numeros_identificacion) == 6:
        intentos_fallidos = 0
        return "Número de cliente validado. Hola Carlos, puedo ayudarte con; 1) Conocer detalle de su deuda vencida, 2) formas y lugares de pago o 3) Solicitar recibo. Coméntanos. ¿Qué necesitas?"
    
    intentos_fallidos += 1
    if intentos_fallidos >= 2:
        return "Número de cliente inválido. Por favor, ingresa un número de 6 dígitos."
    return "Demasiados intentos fallidos. Por favor, intenta más tarde."

def deuda():
    """ Cuando se valida solo consumira el mensaje de Carlos para demostrar que esta validado """

    nombre = "Carlos"

    return f"""{nombre} Tienes un recibo pendetiente de tu servicio MOVIL 
            001 que venció el 01/12 por $30.000. ¿Contamos con tu pago para hoy o mañana?"""

def recibo():
    """ Arrojará un mensaje con respecto al recibo, cuando el usuario dice que pagará hoy también cae acá  """

    b2c= "Obten tu recibo con solo unos clics https://mirecibo.movistar.com.pe/"
    

    return f"{b2c} se esta cargando el pdf con los datos..."

def lugaresPago():
    """ Mostra el mensaje de lugares donde pagar """

    return """En Movistar te brindamos diversas formas de pago SIN COMISION. Puedes pagar por Yape
    https://innovacxion.page.link/mVFa. 
    Desde la web o app de tu banco. Conoce todos los canales de pago en el siguiente link
    https://www.movistar.pe/atencion-al-cliente/lugares-y-medios-de-pago
    """

def esDespedida(mensaje_usuario: str) -> bool:
    """ detecta el mensaje para salir de la conversacion """
    despedidas = ["adios", "hasta luego", "chao", "nos vemos", "gracias", "muchas gracias"]
    mensaje_usuario = mensaje_usuario.lower()
    return any(despedida in mensaje_usuario for despedida in despedidas)   

def despedida():
    """ arroja el mensaje de despedida """

    return "Gracias por usar los servicios de Movistar. ¡Que tengas un buen día!"

def esperarPago():
    """ Este mensaje aparece cuando el usuario comenta que pagará el día de mañana, después de estar arrojar el mensaje de deuda """

    return "Perfecto, guardaremos en el sistema que mañana pagará. ¿Necesita realizar algun otro requerimiento?"

def otroServicio():
    """ Esta funcion aparece cuando el usuario pregunta por otros servicios de Movistar """

    return "Lamento informar que solo puedo optener información de, 1) Conocer detalle de su deuda vencida, 2) formas y lugares de pago o 3) Solicitar recibo, para más información por favor llamar al 600 600 600"

def fueraContexto():
    """ Esta funcion aparece cuando el usuario saca de contexto al Chat """

    return "Lo siento mucho, pero solo puedo brindar ayudar con Movistar. ¿Eres cliente Movistar?"

@app.post("/chat")
def ask_movistar(user: User):
    global historial_conversacion
    print("soy un historial", historial_conversacion)
    user_message = user.user_message.strip()
    if not user_message: 
        return {"message": "Por var, introduzca un mensaje"}
    contexto_bot = [{"role":"system", "content": "Eres un asistente virtual llamado REL Movistar, posees las siguientes funciones: bienvenida, validarCliente, deuda, recibo, lugaresPago, fueraContexto, esMovistar, esperarPago, otroServicio, nombre. Tu objetivo es decidir cual funcion utulizar para responderle al clente."},
                    {"role": "user", "content": "Como te llamas?"},
                    {"role": "assistant", "content": "Soy REL asistente de Movistar.Y puedo ayudarte con; 1) Conocer detalle de su deuda vencida, 2) formas y lugares de pago o 3) Solicitar recibo."}]
    historial_conversacion.append({"role": "user", "content": user.user_message})
    

    # Define las herramientas disponibles
    tools = [
        {"type": "function", "function": {"name": "bienvenida", "description": "Mensaje de bienvenida", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "validarCliente", "description": "Busca al usuario en la Base de datos", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "deuda", "description": "Mensaje de deuda", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "recibo", "description": "Mensaje de recibo", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "lugaresPago", "description": "Mensaje de lugares de pago", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "fueraContexto", "description": "Mensaje si es que se sale de contexto", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "esMovistar", "description": "Mensaje para el usuario que es Movistar", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "esperarPago", "description": "Mensaje para el usuario que es Movistar", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "otroServicio", "description": "Mensaje para mostrar por otros servicio", "parameters": {"type":"object", "properties": {}}}},
        {"type": "function", "function": {"name": "nombre", "description": "Mensaje para mostrar su identidad", "parameters": {"type":"object", "properties": {}}}},
    ]

    # Llamada a la API de OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=contexto_bot+historial_conversacion,
        tools=tools,
        tool_choice="auto",
    )

    # Procesar la respuesta y las llamadas a herramientas
    bot_response = ""

    if esSaludo(user_message):
        bot_response = bienvenida()
    elif esDespedida(user_message):
        bot_response = despedida()
    else:
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                tool_function_name = tool_call.function.name
                if tool_function_name == "bienvenida":
                    bot_response += bienvenida()
                elif tool_function_name == "validarCliente":
                    bot_response += validarCliente(user.user_message)
                elif tool_function_name == "deuda":
                    bot_response += deuda()
                elif tool_function_name == "recibo":
                    bot_response += recibo()
                elif tool_function_name == "lugaresPago":
                    bot_response += lugaresPago()
                elif tool_function_name == "despedida":
                    bot_response += despedida()
                elif tool_function_name == "fueraContexto":
                    bot_response += fueraContexto()
                elif tool_function_name == "esMovistar":
                    bot_response += esMovistar()
                elif tool_function_name == "esperarPago":
                    bot_response += esperarPago()
                elif tool_function_name == "otroServicio":
                    bot_response += otroServicio()
                elif tool_function_name == "nombre":
                    bot_response += nombre()
        
    historial_conversacion.append({"role": "assistant", "content": bot_response})
    return {"message": bot_response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
