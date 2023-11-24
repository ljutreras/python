import requests
import openai
import json
import os
import uuid
from mysql_repository import insert_query
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = FastAPI()
uid = str(uuid.uuid4())
openai.api_key=os.getenv('API_KEY')

class User(BaseModel):
    message: str
    


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = os.getenv('DB_PASSWORD'),
            database = "chatgpt"
        )
        return connection
    except mysql.connector.errors as e:
        print("Error al conectar a MySQL", e)
        return None

connection = connect_to_database()
cursor = connection.cursor()

def get_date_from_external_api():
        """get date from an external api"""
        api_url = os.getenv('DATE_URL')
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error al consumir la API externa. Código de estado: {response.status_code}"}


def get_date_from_body():
    """give an response with an external date"""
    date = get_date_from_external_api()
    return json.dumps({"date": date})

@app.post("/items/")
async def run_conversation(user: User):
        res = user.message
        try:
            # Step 1: send the conversation and available functions to the model
            messages=[
                {
                    'role': 'system',
                    'content':'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha'
                },
                {
                    'role':'user',
                    'content': res
                }
            ]
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_date_from_body",
                        "description": "give an response with an external date, not the wheater",
                        "parameters": {
                            "type": "object",
                            "properties": {}
                        },
                    },
                }
            ]
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                tools=tools,
                tool_choice='auto'
            )
            response_message = response.choices[0].message

            tool_calls = response_message.tool_calls
            # Step 2: check if the model wanted to call a function
            if tool_calls:
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                available_functions = {
                    "get_date_from_body": get_date_from_body,
                }
                messages.append(response_message)  # extend conversation with assistant's reply
                # Step 4: send the info for each function call and function response to the model
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
                    )  # extend conversation with function response
                second_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                )
                
                if connection:
                    cursor.execute(insert_query('users'), (uid, 'user', user.message))
                    cursor.execute(insert_query('assistant'),(uid, second_response.choices[0].message.role, second_response.choices[0].message.content))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
            
                return {'message':second_response.choices[0].message.content}
            else:
                 print(f'else: {response_message}')
                 return {'message': response_message.content}
        except TypeError as e:
            return e
