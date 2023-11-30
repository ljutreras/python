def detalle_de_la_deuda(message: str):
    """proporciona el detalle de la deuda de un usuario mediante un formato predefinido entre triple comillas dobles

    Args:
        message (str): se entregará una opcion valida del servicio detalle de la deuda

    Returns:
        prompt (str): proporciona un detalle de la deuda del usuario
    """        
        
    prompt: str = f"""Tu tarea es dar el detalle de la deuda de un usuario \
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