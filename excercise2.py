from typing import Optional
import requests
import openai
import json
import os
import uuid
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = FastAPI()
openai.api_key=os.getenv('API_KEY')

class User(BaseModel):
    id: Optional[str] = ''
    message: str



def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = os.getenv('DB_PASSWORD'),
            database = "history_chat"
        )
        return connection
    except mysql.connector.errors as e:
        print("Error al conectar a MySQL", e)
        return None

connection = connect_to_database()
cursor = connection.cursor()


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
def pokeapi():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        data = respuesta.json()
        print("respuesta de la API WEB: ", data)
        fecha = data.get('pokemon', 'No disponible')
        return fecha
    else:
        return "Error al obtener la fecha"


def get_current_date():
    fecha_actual = web_fecha()
    return json.dumps({"fecha": fecha_actual})

def get_pokemon():
    pokemon = pokeapi()
    return json.dumps({"pokemon": pokemon})

def insertBD(uid, role, content, function_calling ,id_bot):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        if role == 'user':
            insert_query = "INSERT INTO chats(uid, role, content, function_calling, date, id_bot) VALUES(%s, %s, %s, %s, NOW(), %s)"
            cursor.execute(insert_query, (uid, role, content, function_calling, id_bot))
        elif role == 'assistant':
            insert_query = "INSERT INTO chats(uid, role, content,function_calling, date, id_bot) VALUES(%s, %s, %s, %s, DATE_ADD(NOW(), INTERVAL 1 SECOND), %s)"
            cursor.execute(insert_query, (uid, role, content, function_calling,id_bot))

        connection.commit()
        cursor.close()
        connection.close()


@app.post("/consulta")
def ask_mia(user: User):
    res = []
    connection = connect_to_database()
    cursor = connection.cursor()
    uid = str(uuid.uuid4())
    user_id = uid if user.id == '' else user.id
    query = f"SELECT content FROM chats WHERE uid = '{user_id}' ORDER BY date ASC"
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    connection.close()



    messages=[
                {
                    'role': 'system',
                    'content':'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha y nombrar los pokemones existentes'
                },
                {
                    'role': 'user',
                    'content':user.message
                },
                {
                    'role': 'assistant',
                    'content':''
                }
            ]
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
        },
        {
            "type": "function",
            "function": {
                "name": "get_pokemon",
                "description": "get a pokemon from a specific web page",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
        }
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    for i, valor in enumerate(res):
            role = 'user' if i % 2 == 0 else 'assistant'
            content = str(valor[0]) if isinstance(valor, tuple) else str(valor)

            messages.append({
                'role': role,
                'content': content
            })

    response_content = response.choices[0].message.content if response.choices else ""

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "get_current_date": get_current_date,
            "get_pokemon": get_pokemon
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

        second_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        print(messages)
        insertBD(user_id, 'user', user.message,None , 1)
        insertBD(user_id, 'assistant', second_response.choices[0].message.content,function_name, 1)

        return {'id': user_id, 'message':second_response.choices[0].message.content}

    else:
        print(messages)
        insertBD(user_id, 'user', user.message,None, 1)
        insertBD(user_id, 'assistant', response_content,None, 1)
        return {'id': user_id, "message": response_message.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)