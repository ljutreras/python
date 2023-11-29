#OBJETIVOS DEL CHAT:
#Las respuestas serán entregadas por ti , por lo que deberás idear un sistema que te permita entregar una respuesta predefinida .
#Ninguna respuesta debe ser generada por CHAT GPT.

#FORMATO DEL MENSAJE INICIAL

""" 
    print()
    ¡Hola! Bienvendi@ al chat de Movistar!

Estoy para ayudarte en:

•Conocer detalle de tu deuda vencida
•Formas y lugares de pago
•Solicitar recibo

        Comentanos,¿qué necesitas?

"""


from openai import OpenAI
import json


client = OpenAI()



#Serie de funciones que seran agregadas a tools para ser llamadas por function calling de acuerdo a cada caso de uso requerido

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

#Lista de tools (funciones declaradas)
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

#Primer mensaje de rol system para indicar el comportamiento y logica que debera emplear la AI
messages = [{"role": "system", "content": "Eres un asistente virtual llamado chat Movistar, posees cuatro funciones: detalleDeuda, formasYLugaresDePago, solicitarRecibo. Tu objetivo es determinar cual funcion utilizar para responderle al cliente, los temas que puedes responder para utilizar las funciones son: Detalle de la deuda, Solicitar recibo, Formas y lugares de pago."}]

#system funcional a medias, YA NO ESTA SIENDO UTILIZADO
""" 
role": "system", "content": "Eres un asistente virtual llamado chat Movistar y tu objetivo es entregarle al cliente solo una de las tres solicitudes que estan dentro de las comillas angulares, en el caso de que el cliente intente preguntarte otra cosa, debes indicarle que solo puedes responder a una de las siguientes solicitudes solicitadas: <Detalle de la deuda>,<Solicitar recibo>,<Formas y lugares de pago>.

 """


#MENSAJE INICIAL
print("        ¡Hola! Bienvendi@ al chat de Movistar!\n\nEstoy para ayudarte en:\n•Conocer detalle de tu deuda vencida\n•Formas y lugares de pago\n•Solicitar recibo\n        Comentanos,¿qué necesitas?\n")

#Input inicial antes de entrar al ciclo while
clientInput = input("Cliente: ").lower()

while clientInput != "exit":

    #Aqui se agrega a la lista messages el input inicial que ingreso el cliente
    messages.append({"role":"user","content":clientInput})

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages= messages,
    tools=tools,
    tool_choice="auto")

    #Respuesta que nos retorna la IA
    response_message = response.choices[0].message

    #PRINTS PARA VER LO QUE NOS RETONRA RESPONSE_MESSAGE###
    """ print("")
    print("RESPONSE MESSAGE:")
    print(response_message)
    print("") """
    #######################################################

    #Variable(tool_calls) que almacenará la lista de diccionarios de la informacion de la funcion que la AI utilizó
    tool_calls = response_message.tool_calls

    #Se consulta si se utilizo alguna tool
    if tool_calls:
  
        #Diccionario que almacenará los los nombres de las funciones disponibles
        available_functions = {
        
        "detalleDeuda": detalleDeuda,
        "formasYLugaresDePago": formasYLugaresDePago,
        "solicitarRecibo": solicitarRecibo,
        
        }

        #Se agrega el mensaje que respondio la IA a la lista messages
        messages.append(response_message)

        # A continuacion se aprecia un ciclo for para recorrer todas las funciones que fueron utilizadas por medio de tools, en cada ciclo se agregaran los datos de "name" y "content" a las variables function_name("El nombre de la funncion se utilizó") y function_response(el contenido que retorno la funcion utilizada, para encontrar estos contenidos dirigirse a los "returns" de cada funcion).

        #Finalmente se agrega a la lista messages un diccionario con las claves "tool_call_id"(id generado al llamar a la funcion),"role"(hardcoded a "tool"), "name"(el nombre de la funcion que se utilizó) y "content"(Contenido que retorno la funcion utilizada)
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


        #Se obtiene la respuesta final de openai en formato string, esto porque accedemos a message.content, luego se agrega a la lista de diccionarios, messages, el chatMovistarMessage que vendria siendo la respuesta final de openai
        
        #Variable que contiene un string vacio
        chatMovistarMessage = ""

        #Diccionario que recibe un string proveniente de function_response (que vendria siendo el contenido que retorna la funcion al ser utilizada), y luego cambia su tipo de dato a diccionario con la fucnion "eval()"
        dictionary = eval(function_response)
        
        #El siguiente ciclo for recorre el diccionario "dictionary" obteniendo solo sus claves mediantes la funcion "values()" para luego asignarlos a la variable "content" en cada ciclo, a su vez dentro de cada ciclo realizado se cambia el tipo de dato de "content" mediante la clase "str()" para luego agregarlo al string "chatMovistarMessage" (los string que se vayan agregando estaran separados por un espacio vacio)
        for content in dictionary.values():
            chatMovistarMessage += str(content)

        #Se agrega a la lista messages la variable "chatMovistarMessage" con role "assistant" ya que se considera que esta es la respuesta que entrego la IA
        messages.append({"role":"assistant","content":chatMovistarMessage})

        #PRINTS PARA VER LA LISTA HISTORICA DE LOS MENSAJES DEL CHAT#####

        """ print("Lista historica de mensajes del chat:")
        print(messages)
        print("") """
        
        ##################################################################
        print("\nChat Movistar: " + chatMovistarMessage)

        #Se vuelve a solicitar un input para ver si el cliente tiene alguna otra consulta o quiere terminar el chat ingresando "exit"
        clientInput = input("\nCliente: ").lower()


    else:

        #Mensaje predeterminado establecido, que sera utilizado en caso de que el cliente no ingrese algun input que accione el uso de las funciones disponibles
        chatPorDesviacionDeTema = "Lo siento, Solo puedo responder a una de las 3 siguientes solicitudes:\n\n• Detalle de la deuda\n• Solicitar recibo\n• Formas y lugares de pago"

        #Se agrega este mensaje predeterminado a la lista "messages" ya que se considera como la respuesta de la IA
        messages.append({"role":"assistant","content":chatPorDesviacionDeTema})

        #PRINTS PARA VER LA LISTA HISTORICA DE LOS MENSAJES DEL CHAT#####

        """ print("Lista historica de mensajes del chat:")
        print(messages)
        print("") """

        ##################################################################
        
        #Se imprime el mensaje predeterminado para indicarle al cliente que debe ingresar una solicitud que sea valida segun los casos de uso
        print("\nChat Movistar: " + chatPorDesviacionDeTema)


        #Se vuelve a solicitar un input para ver si el cliente tiene alguna otra consulta o quiere terminar el chat ingresando "exit"
        clientInput = input("\nCliente: ").lower()

#######################################################################################################################################
