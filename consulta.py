from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.environ['API_KEY'])

class User(BaseModel):
    user_message: str



def bienvenida():
    """
    Cual quier saludo, el bot responderá con algo de acá 
    """
    text = """
    Soy un agente de Movistar y estoy aquí para ayudarte. ¿Por favor me puedes proporcionar la identificacion de id?
    """

    prompt =f"""
    Eres un agente virtual de MOVISTAR y solo puedes responder con el {text} después del saludos
    """
    return prompt

def validarCliente():
    """ Acepta cualquier cantidad de numero de identificación. Si uno escribe que su numero de identificacion es xx, aun que sean dos. arroja este mensaje  """

    text= "Validado con la base de datos, le puedo ayudar con los siguiente temás 1) Detalle de deuda vencida, 2) Formas y lugares de pago o 3) Solicitud de recibo"

    prompt= f"""
    Responde con el {text} cuando los digitos de la indentificacion sean seis numeros
    """
    return prompt

def noEncontrado():
    """ Si el usuario escribe menos de 5 numeros, el chat debe arrojar estos mensajes """

    text1= "lo sentimos el usuario no fue encontrado en la base de datos, por favor vuelva a intentar"
    text2= "Lo sentimos no pudimos validar tu identidad. Intenta más tarde. Que tengas buen día."

    prompt = f"""
    Responde con el {text1} cuando los digitos de la identificacion sean menores a cinco
    Si intenta más de dos veces {text2}
    """
    return prompt

def deuda():
    """ si el usuario escribe que quiere ver su deuda  """

    text = f"""
    Detalle de la deuda
    Carlos Tienes un recibo pendiente de tus servicio MOVIL 
    001 que vencio el 29/11 por $30.000
    Contamos con tu pago para hoy o mañana?
    """

    prompt = f"""
    cuando el usuario diga deuda responde con {text} interpreta la fecha dentro de los signos <> {text}
    """
    return prompt

def recibo():
    """ Si el usuario escribe que esta interesado del recibo """

    text="""B2C: obten tu recibo con solo clics http://mirecibo.movistar.com.pe/.
    B2B: Se esta validando que en la base de asignación vaya el link del pdf del recibo    
    """
    prompt = f"""
    cuando el usuario diga recibo responde con {text}
    """
    return prompt

def lugaresPago():
    """ Si el usuario escribe algo relacionado con los lugares de pago """

    text="""
    En Movistar te brindamos diversas formas de pago SIN COMISIÓN. Puedes pagar por Yape http://innovacxion.page.link/mVFa.
    desde la web o app de tu banco. Conoce todo los canales de pago en el siguiente link:
    https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago
    """
    prompt = f"""
    Cuando el usuario diga formas o lugares de pago responde con {text}
    """
    return prompt

def despedida():
    """ Después que el usuario diga que pagará hoy o mañana, arrojará este mensaje """
    text = "Gracias por contactarnos, que tengas un excelente día!"

    text2 = ""

    prompt = f"""
    Después de que el usuario diga que pagará hoy o mañana la deuda, arrojar este mensaje {text}

    si dice otro día, pedirle amablemente si puede pagar hoy o mañana
    """
    return prompt

@app.post("/chat")
def ask_movistar(user: User):

    # Llamada a la API de OpenAI   
    message = [
        {
            "role": "user", "content": user.user_message
        },
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "bienvenida",
                "description": "Obtiene el mensaje despues del saludo",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "validarCliente",
                "description": "Obtiene el cliente dentro de la base de datos",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "noEncontrado",
                "description": "Obtiene el cliente no encontrado en la base de datos",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "deuda",
                "description": "Obtiene la deuda del cliente",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "recibo",
                "description": "Obtiene el recibo del cliente",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "lugaresPago",
                "description": "Obtiene los lugares para pagar",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "despedida",
                "description": "Obtiene los lugares para pagar",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }

    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=message,
        tools=tools,
        tool_choice="auto",
        temperature=0.3,
        top_p=0.95
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "bienvenida": bienvenida,
            "validarCliente": validarCliente,
            "noEncontrado": noEncontrado,
            "deuda": deuda,
            "recibo": recibo,
            "lugaresPago": lugaresPago,
            "despedida": despedida,

        }
        message.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_response = function_to_call()
            message.append(
                {
                    "tool_call_id": tool_call.id,
                    "role" : "tool",
                    "name": function_name,
                    "content": function_response
                }
            )
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=message,
            tools=tools,
            tool_choice="auto",
            temperature=0.3,
            top_p=0.95
            )

        function_calling = "none"

        tool_calls = response_message.tool_calls
        if tool_calls:
            function_calling = tool_calls[0].function.name

        botResponse = second_response.choices[0].message.content

        return {"message": botResponse}


    oneResponse = response.choices[0].message.content

    return {"message": oneResponse}

if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)