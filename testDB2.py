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

conectionFindUser = conectionDB()



cursorFindRole = conectionFindUser.cursor()

#cursorFindContent = conectionFindUser.cursor()

mensaje = []
dictionary = {}
voidTuple = []

contentChatsByUid = f"SELECT content FROM chats where uid = '27d115067cd7402a9a32070c47eb75dd' order by date asc"
roleChatsByUid= f"SELECT role, content,function_calling FROM chats order by date asc"

cursorFindRole.execute(roleChatsByUid)

#cursorFindContent.execute(contentChatsByUid)



#recordUser = cursorFindContent.fetchall()
recordRole = cursorFindRole.fetchall()


for role, content,function_calling in recordRole:
    
    dictionary = {"role":role,"content":content,"function_calling":function_calling}

    voidTuple.append(dictionary)

print(voidTuple)



""" for content in recordRole:
    voidTuple.append("".join(content))


cursorFindRole.execute(contentChatsByUid)
recordRole = cursorFindRole.fetchall()

for content in recordRole:
    index= content.index(content)
    voidTuple.insert(index + 1,"".join(content))
    


print(voidTuple)

 """
""" for content in recordRole:

    contenido = "".join(content)
    dictionary.
    print(contenido)
 """




""" tuple = content
#print(tuple)
 """

#cursorFindContent.close()
conectionFindUser.close()

