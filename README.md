## Importante
El chat se mantiene en uso siempre y cuando el servidor este levantado, para reiniciarlo se recomiendo bajar el servicor y volver a levantar.

## Chat-Bot 
El uso de un chat bot interctuando con el cliente

## Instalar las librerías necesarias 
pip install -r REQUIREMENTS.txt
Tener instalado Postman

# Tener la variable de entorno 
De forma local en un archivo .env

## Uso
# 1) Levantando el sistema de uvicorn escribiendo:
uvicorn consulta:app --reload

# 2) Ahora en postman:
Seleccionamos Body --> raw --> y en la lista que sale a la izquierda marcamos Json

Copiamos la url:
http://127.0.0.1:8000/chat

y en el body debe quedar:

{
    "user_message": "Quiero pagar mañana "
}

![image](https://github.com/ljutreras/python/assets/94999914/fe3506bd-5750-410a-bf33-6e377454fc6b)
Algo así debería quedar


   