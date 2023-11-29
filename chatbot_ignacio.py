""" 

Las respuestas serán entregadas por ti , por lo que deberás idear un sistema que te permita entregar una respuesta predefinida .

Ninguna respuesta debe ser generada por CHAT GPT.

"""

###INICIA LA CONVERSACION


""" 
    print()
    ¡Hola! Bienvendi@ al chat de Movistar!

Estoy para ayudarte en:

•Conocer detalle de tu deuda vencida
•Formas y lugares de pago
•Solicitar recibo

        Comentanos,¿qué necesitas?



"""



import requests
from openai import OpenAI
import json

""" class User(BaseModel):
    message: str """

client = OpenAI()





def detalleDeuda():
    """Obtener el detalle de la deuda vencida"""

    nombre = "Ignacio"
    servicio = "movil"
    nro_servicio = "12345"
    fecha = "08/07"
    monto_deuda = str(100)

    return json.dumps({"nombre": f"{nombre} tienes un recibo pendiente de tu servicio {servicio} {nro_servicio} que vencio el {fecha} por {monto_deuda}. ¿Contamos con tu pago para hoy o mañana?"})

def formasYLugaresDePago():
    """Obtener las formas y lugares de pago"""

    firstParagraph = "En Movistar te brindamos diversas formas de pago SIN COMISIÓN. Puedes para por Yape: "
    secondParagraph = ", desde la web o app de tu banco. Conoce todos los canales de pago en el siguiente link: "

    return json.dumps({"primer parrafo":firstParagraph,"pagina web para pagar": "https://innovacxion.page.link/mVFa","segundo parrafo":secondParagraph,"canal de pago":"https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago"})

def solicitarRecibo():
    """Obtener el recibo"""
    defaultMessage = "Obten tu recibo con solo unos clics: "
    b2c = "https://mirecibo.movistar.com.pe/"
    
    return json.dumps({"mensaje predeterminado":defaultMessage,"url del recibo": b2c})


tools = [
        {
            "type": "function",
            "function": {
                "name": "detalleDeuda",
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
                "name": "formasYLugaresDePago",
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
                "name": "solicitarRecibo",
                "description": "Obtener el recibo",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        }]


messages = [{"role": "system", "content": "Eres un asistente virtual llamado chat Movistar, posees cuatro funciones: detalleDeuda, formasYLugaresDePago, solicitarRecibo. Tu objetivo es determinar cual funcion utilizar para responderle al cliente, los temas que puedes responder para utilizar las funciones son: Detalle de la deuda, Solicitar recibo, Formas y lugares de pago."}]

#funcional a media
""" 
role": "system", "content": "Eres un asistente virtual llamado chat Movistar y tu objetivo es entregarle al cliente solo una de las tres solicitudes que estan dentro de las comillas angulares, en el caso de que el cliente intente preguntarte otra cosa, debes indicarle que solo puedes responder a una de las siguientes solicitudes solicitadas: <Detalle de la deuda>,<Solicitar recibo>,<Formas y lugares de pago>.

 """


#MENSAJE INICIAL
print("        ¡Hola! Bienvendi@ al chat de Movistar!\n\nEstoy para ayudarte en:\n•Conocer detalle de tu deuda vencida\n•Formas y lugares de pago\n•Solicitar recibo\n        Comentanos,¿qué necesitas?")

clientInput = input("Cliente: ").lower()

while clientInput != "exit":

    
    messages.append({"role":"user","content":clientInput})

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages= messages,
    tools=tools,
    tool_choice="auto")


    response_message = response.choices[0].message
    print("")
    print("RESPONSE MESSAGE:")
    print(response_message)
    print("")
    tool_calls = response_message.tool_calls


    if tool_calls:
  

        available_functions = {
        
        "detalleDeuda": detalleDeuda,
        "formasYLugaresDePago": formasYLugaresDePago,
        "solicitarRecibo": solicitarRecibo,
        #"respuestaPorDesviacionDeTema": respuestaPorDesviacionDeTema

        
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

        """ second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0
        ) """

        #Se obtiene la respuesta final de openai en formato string, esto porque accedemos a message.content, luego se agrega a la lista de diccionarios messages el chatMovistarMessage que vendria siendo la respuesta final de openai
        
        chatMovistarMessage = ""
        dictionary = eval(function_response)
        

        for content in dictionary.values():
            chatMovistarMessage += str(content)

        messages.append({"role":"assistant","content":chatMovistarMessage})

        print("Lista historica de mensajes del chat:")
        print(messages)
        print("")
        
        print("Chat Movistar: ", chatMovistarMessage)

        print("")

        clientInput = input("Cliente: ").lower()


    else:

        #chatMovistarMessage = response.choices[0].message.content
        chatPorDesviacionDeTema = "Lo siento, Solo puedo responder a una de las 3 siguientes solicitudes: Detalle de la deuda, Solicitar recibo, Formas y lugares de pago"
        messages.append({"role":"assistant","content":chatPorDesviacionDeTema})

        print("Lista historica de mensajes del chat:")
        print(messages)
        print("")

        print("Chat Movistar: " + chatPorDesviacionDeTema)
        print("")
        clientInput = input("Cliente: ").lower()



#######################################################################################################################################
