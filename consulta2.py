from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from mysql.connector import Error
from typing import Optional
import mysql.connector
import requests
import openai
import json
import uuid
import os

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.environ['API_KEY'])

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='history_chat',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print("Error al conectar a MySQL", e)
        return None

class UserRequest(BaseModel):
    uid: Optional[str] = ""
    user_message: str

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

def insertBD(uid, role, content, id_bot):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        try:
            if role == 'user':
                insert_query = "INSERT INTO chats(uid, role, content, id_bot) VALUES(%s, %s, %s, %s)"
                cursor.execute(insert_query, (uid, role, content, id_bot))
            elif role == 'assistant':
                insert_query = "INSERT INTO chats(uid, role, content, id_bot) VALUES(%s, %s, %s, %s)"
                cursor.execute(insert_query, (uid, role, content, id_bot))
            
            connection.commit()
        except Error as e:
            print("Error al insertar en la base de datos:", e)
        finally:
            cursor.close()
            connection.close()
    else:
        print("No se pudo conectar a la base de datos")



@app.post("/consulta")
def ask_mia(request: UserRequest):
    randomUid = str(uuid.uuid4()).replace("-","")
    uidChat = randomUid if request.uid == "" else request.uid

    conectionFindUser = connect_to_database()
    cursoFinderUser = conectionFindUser.cursor()

    if request.uid:

        d = {}
        messages = []

        contentChatsByUid = f"SELECT role, content FROM chats where uid = '{request.uid}' order by date ASC"

        cursoFinderUser.execute(contentChatsByUid)
        record = cursoFinderUser.fetchall()

        for role, content in record:
            d = {"role": role, "content": content}
            messages.append(d)
        messages.append({"role": "user", "content": request.user_message})
        print(messages)
    else:
        messages = [{"role": "system", "content": "Eres un agente virutal llamada Mia y tu objetivo es retornar la fecha actual."}, {"role": "user", "content": request.user_message}]

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
        messages=messages,
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
            function_response = function_to_call()
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

        conection = connect_to_database()
        if conection:
            cursor = conection.cursor()

            queryInsertUser = ("INSERT into chats(uid, role, content, function_calling, id_bot) VALUES(%s, %s, %s, %s)")
            queryInsertAssistant = ("INSERT into chats(uid, role, content, function_calling, id_bot) VALUES(%s, %s, %s, %s)")

            botResponse = second_response.choices[0].message.content

            cursor.execute(queryInsertUser, (uidChat, "user", request.user_message, "none", 1))
            cursor.execute(queryInsertAssistant, (uidChat, "assistant", botResponse, 1))

            conection.commit()
            cursor.close()
            conection.close()

        return{
            "uid": uidChat,
            "message": second_response.choices[0].message
        }
    
    else: 
        conection = connect_to_database()
        if conection:

            cursor = conection.cursor()

            queryInsertUser = ("INSERT into chats (uid, role, content, id_bot) VALUES(%s, %s, %s, %s)")
            queryInsertAssistant = ("INSERT into chats (uid, role, content, id_bot) VALUES(%s, %s, %s, %s)")

            botResponse = response_message.content

            cursor.execute(queryInsertUser, (uidChat, "user", request.user_message, 1))
            cursor.execute(queryInsertAssistant, (uidChat, "assistant", botResponse, 1))

            conection.commit()
            cursor.close()
            conection.close()

    return {"uid": uidChat, "message": response_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
