def formas_y_lugares_de_pago(message):
    prompt = f"""Tu tarea es dar la informacion de formas y lugares de pago



            luego debes retornar el contenido delimitado por triple comillas dobles. \
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
