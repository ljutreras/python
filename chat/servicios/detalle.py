def detalle_de_la_deuda(message):
    prompt = f"""Tu tarea es dar el detalle de la deuda de un usuario

            Primero debes retornar un mensaje \"necesito consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad DNI numerico del titular del servicio\"\
            el documento de identidad del titular debe ser su DNI en formato de tipo numerico de maximo 9 caracteres y minimo 8 caracteres \
            si el usuario ingresa otro mensaje, debes repetir de que ingrese el DNI del titular \
            luego retornas el contenido delimitado por triple comillas dobles. \
            \"\"\"DETALLE DE LA DEUDA
            Estimado client@ cuyo registro termina en <DNI> 
            Tienes un recibo pendiente de tu servicio <MOVIL/HOGAR> N° Servicio 7556 
            que venció el 09/23 por CLP 25.000\"\"\"

            para el campo DNI le asignaras los 4 ultimos digitos del contenido delimitado por triples comillas invertidas
            para el campo MOVIL/HOGAR eligiras una de las 2 opciones mencionadas
            
            luego le preguntarás al usuario si hay algo más en que lo pueda ayudar \
            
            la informacion obtenida será delimitada por triples comillas invertidas.\

            mensaje del usuario: ```{message}```
            """
    return prompt
