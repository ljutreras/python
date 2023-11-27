from fastapi import FastAPI
import requests
import openai
from pydantic import BaseModel
from openai import OpenAI
import json
import uuid
import mysql.connector
from typing import Optional

#############################################################

def conectionDB():
    host = "localhost"
    user = "root"
    password = ""
    database = "history_chat"

# Crear un objeto de conexión
    conection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    return conection

###########################################################

app = FastAPI()

client = OpenAI()

class User(BaseModel):
    uid: Optional[str] = ""
    message: str
    

def web_fecha():
    url = 'http://disal.mibot.cl/api2.php'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        data = respuesta.json()
        print("respuesta de la API WEB: ", data)
        fecha = data.get('fecha_actual', 'No disponible')
        return fecha
    else:
        return "Error al obtener la fecha"

def get_current_date():
    fecha_actual = web_fecha()
    return json.dumps({"fecha": fecha_actual})



@app.post("/consulta")
def comunicacionOpenAI(user: User):

    randomUid = str(uuid.uuid4()).replace("-", "")
    uidChat = randomUid if user.uid == "" else user.uid

    conectionFindUser = conectionDB()
    cursorFindUser = conectionFindUser.cursor()


    
    
    #A continuacion se consulta si se ingreso un uid en el body de postman
    if user.uid:
        
        #Se definen un diccionario y una lista para ser llenados dentro de este "if"
        dictionary = {}
        messages = []
        #print(user.uid)

        #A continuacion se define una variable que contendra la query para mysql donde se obtendran las filas de las columnas "role" y "content" de la tabla "chats", se obtienen con un "where uid = user.uid" para conseguir solo las filas que compartan este identificador (que fue obtenida )
        contentChatsByUid = f"SELECT role,content FROM chats where uid = '{user.uid}' order by date ASC" #agregar oder by date de forma acendente

        #print(contentChatsByUid)

        cursorFindUser.execute(contentChatsByUid)
        record = cursorFindUser.fetchall()

        for role, content in record:
            dictionary = {"role":role,"content":content}
            messages.append(dictionary)
        messages.append({"role": "user", "content": user.message})
        print(messages)

    #En este caso se considera como si NO se ingreso un uid en el body de postman por ende, se determina que el primer diccionario o comando que se le otorgara a "messages" sera un "role": "system" ademas del primer mensaje que usuario va a enviar en su conversacion
    else:
        messages = [{"role": "system", "content": "Eres una agente virtual llamada Mia y tu objetivo es retornar la fecha actual."},{"role": "user", "content": user.message}]
    


    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Get the current date from a specific web page",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        }
    ]
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages= messages,
    tools=tools,
    tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls



    if tool_calls:

        available_functions = {
            "get_current_date": get_current_date,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_response = function_to_call(
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        ) 

        conection = conectionDB()
        if conection:

            cursor = conection.cursor()
            

            #El id se debera generar solo si no habia un uid de chat anteriormente creado

            queryInsertUser = ("INSERT into chats(uid, role, content, id_bot) VALUES (%s, %s, %s,%s)")
         
            queryInsertAssistant = ("INSERT into chats(uid, role, content, id_bot) VALUES (%s, %s, %s,%s)")

            botResponse = second_response.choices[0].message.content

            cursor.execute(queryInsertUser,(uidChat,"user",user.message, 1))
            cursor.execute(queryInsertAssistant,(uidChat,"assistant",botResponse,1))

            conection.commit()
            cursor.close()
            conection.close()


        return {
            "uid":uidChat,
            "message":second_response.choices[0].message
            }
    
    else:

        conection = conectionDB()
        if conection:

            cursor = conection.cursor()
            

            #El id se debera generar solo si no habia un uid de chat anteriormente creado

            queryInsertUser = ("INSERT into chats(uid, role, content, id_bot) VALUES (%s, %s, %s,%s)")
         
            queryInsertAssistant = ("INSERT into chats(uid, role, content, id_bot) VALUES (%s, %s, %s,%s)")

            botResponse = response_message.content

            cursor.execute(queryInsertUser,(uidChat,"user",user.message, 1))
            cursor.execute(queryInsertAssistant,(uidChat,"assistant",botResponse,1))

            conection.commit()
            cursor.close()
            conection.close()

        return {"uid":uidChat,"message":response_message}



