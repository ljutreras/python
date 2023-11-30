
# CHATBOT MOVISTAR

Asistente virtual diseñado para entregar información sobre un servicio telefonico en base a la inteligencia artificial de OpenAI


## Primeros pasos

1.- Es recomendable trabjar en base a un entorno virtual, para ello utilizaremos el siguiente comando desde nuestra consola.

```bash
  python -m venv venv
```

2.- Ya tienes tu entorno virtual? perfecto! solo nos queda activarla, para ello utilizaremos el siguiente comando

#### Forma 1
```bash
  source c:/ruta/de/carpeta/python/venv/Scripts/activate
```
#### Forma 2
Desde VSCode haremos lo siguiente
```
  CTRL + SHIFT + P
  Python: Select Interpreter
  ⭐​Python 3.12.0 ('venv': venv) Recommended
```

3.- Lo siguiente que debes realizar es la instalacion de las librerias para nuestro proyecto, para ello he proporcionado un archivo REQUIREMENTS.txt el cual se instala de la siguiente manera

```bash
  pip install -r REQUIREMENTS.txt
```

4.- Perfecto! ya casi lo tienes, solo quedaria generar un archivo .env para poder agregar el token que te permitirá utilizar la aplicación

```
    API_KEY='sk-token_de_openai'
```

#### ⛔​ ​Por temas de seguridad no puedo proporcionar el token, se que lo entenderás ⛔​


## Ya solo queda ejecutar nuestra aplicación

1.- Desde la consola nos situamos en la carpeta chat de nuestro proyecto

```bash
cd chat
```

2.- Ejecutamos nuestra aplicación con el comando

```bash
py main.py
```

## 🥳 Felicidades! Ya tienes todo lo necesario para interactuar con la aplicación 🥳
