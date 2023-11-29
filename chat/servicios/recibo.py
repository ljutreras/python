def solicitar_recibo(message):
    prompt = f"""Tu tarea es dar la informacion de donde solicitar el recibo
                        
            siempre y cuando hayas obtenido el DNI debes retornar el contenido delimitado por triple comillas dobles a continuación. \
            \"\"\"SOLICITAR RECIBO \n \
            Obten tu recibo con solo unos clics \n \
            https://mirecibo.movistar.com.pe\"\"\"
            
            si el usuario no ha proporcionado el DNI, debes volver a solicitarlo

            el campo DNI debe ser proporcionado por el usuario
            luego le preguntarás al usuario si hay algo más en que lo pueda ayudar \
            si el usuario ya ingresó el documento de identidad, no volver a solicitarlo \

            la informacion obtenida será delimitada por triples comillas invertidas.\
            datos del usuario: ```{message}```
            """
    return prompt

""" 


primero retornas un mensaje mencionando que necesitas consultar 
algunos datos para continuar con tu consulta. 
Por favor, ingresa el documento de identidad DNI numerico del titular del servicio\


el documento de identidad del titular debe ser su DNI en formato de tipo numerico de maximo 9 caracteres y minimo 8 caracteres \
si el usuario ingresa otro mensaje, debes repetir de que ingrese el DNI del titular \

 """