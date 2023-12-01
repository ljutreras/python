def despedida(message: str):
    """ proporciona un mensaje de despida junto a un resumen de lo conversado

    Args:
        message (str): obtendra un mensaje con intencion de terminar la conversación

    Returns:
        prompt (str): retornara un mensaje de despedida junto a un resumen de lo conversado
    """        
    prompt: str = f"""Tu tarea es dar un resumen de lo conversado además de despedirse en un estilo amigable breve y muy conversacional\        
                
            Primero debes identificar si hay una intención de despedida por parte del mensaje  \
            luego finalizarás la conversación mostrarás un resumen de la conversacion mediante el siguiente contenido descrito entre comillas triples \
            \"\"\" 
            <DETALLE DE LA DEUDA>
            <FORMAS Y LUGARES DE PAGO>
            <SOLICITUD DE RECIBO>
            recuerda que con la palabra \"salir\" puedes finalizar el chat
            \"\"\" \
            el campo <DETALLE DE LA DEUDA> <FORMAS Y LUGARES DE PAGO> y <SOLICITUD DE RECIBO> serán proporcionado por la asistente siempre y cuando hayan sido solicitados previamente\
            de lo contrario el campo quedará vacio \
            la informacion obtenida será delimitada por triples comillas invertidas.\

            mensaje del usuario: ```{message}```
            """
    return prompt