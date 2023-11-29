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

# clientInput = input()

# clientAskFunction = validateFunction(clientInput)

#if clientAskFunction == True


""" 
print()
Necesito consultar algunos datos para
continuar con tu consulta.Por favor, ingresa
el documento de identidad del titular del
servicio

"""

#if clientInDB == False

#   if attemptsDB > 2 :
#       print("Disculpa no pudimos validar tu identidad, intenta mas tarde")
#   else:
#       print("No fue posible validar tu identidad. Por favor intenta nuevamente")


#else:

#   for function in functionList
#       


import requests
from openai import OpenAI
import json


client = OpenAI()

"""
    def get_current_date():
        fecha_actual = web_fecha()
        return json.dumps({"fecha": fecha_actual}) 
    
"""

messages = []

def detalleDeuda():
    """Obtener el detalle de la deuda vencida"""

    nombre = "Ignacio"
    servicio = "movil"
    nro_servicio = ""
    fecha = "dd/mm"
    monto_deuda = str(100)

    return json.dumps({"nombre": nombre},{"servicio": servicio},{"numero servicio": nro_servicio},{"fecha": fecha},{"monto deuda": monto_deuda})

def formasYLugaresDePago():
    """Obtener las formas y lugares de pago"""

    return json.dumps({"pagina web para pagar": "https://innovacxion.page.link/mVFa"},{"canal de pago":"https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago"})

def solicitarRecibo():
    """Obtener el recibo"""
    

    return json.dumps({"": ""})

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

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages= messages,
    tools=tools,
    tool_choice="auto")

#MENSAJE INICIAL
print("        ¡Hola! Bienvendi@ al chat de Movistar!\n\nEstoy para ayudarte en:\n•Conocer detalle de tu deuda vencida\n•Formas y lugares de pago\n•Solicitar recibo\n        Comentanos,¿qué necesitas?")

#Lista de funciones: Detalle de la deuda, Solicitar recibo, Formas y lugares de pago
functionList = ["deuda","recibo","pago"]

#Input del cliente
clientInput = input("Cliente: ").lower()

#Funcion para validar si lo que ingreso el cliente esta dentro de las funciones disponibles, de ser asi retorna True, caso contrario retorna False

def stringTolist(string):
    return string.split()

def validateInput(clientInput):

    validator = False
    clientInputList = stringTolist(clientInput)

    for function in functionList:
        for inputWord in clientInputList:
            print(inputWord,function)
            if inputWord == function.lower():
                
                validator = True
                break
        
        

    return validator


prueba = validateInput(clientInput)
#pruebaLista = stringTolist("Hola mi nombre es Ignacio")
print(prueba)
#print(pruebaLista)
