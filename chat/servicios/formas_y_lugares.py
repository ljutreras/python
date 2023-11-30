def formas_y_lugares_de_pago(message):
    prompt = f"""Tu tarea es limitarte a dar la informacion de formas y lugares de pago

                Primero debes retornar un mensaje \"necesito consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad DNI numerico del titular del servicio\"\
                el documento de identidad del titular debe ser su DNI en formato de tipo numerico de maximo 9 caracteres y minimo 8 caracteres \
                si el usuario ingresa otro mensaje, debes repetir de que ingrese el DNI del titular \
                para ello debes retornar el contenido delimitado por triple comillas dobles a continuacion. \
                \"\"\"FORMAS Y LUGARES DE PAGO 
                En Movistar te brindamos diversas formas de pago SIN COMISIÓN. \
                Puedes pagar por Yape \
                https://innovacxion.page.link/mVFa \
                desde la web o app de tu banco. \
                Conoce todos los canales de pago en el siguiente link \
                https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago\"\"\"
                
                luego le preguntarás al usuario si hay algo más en que lo pueda ayudar \
                
                la informacion obtenida será delimitada por triples comillas invertidas.\

                datos del usuario: ```{message}```
            """
    return prompt
