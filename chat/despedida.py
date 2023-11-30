def despedida(message):
    prompt = f"""Tu tarea es dar un resumen de lo conversado además de despedirse en un estilo amigable breve y muy conversacional\        
            
            Primero debes identificar si hay una intención de despedida por parte del mensaje  \
            luego finalizarás la conversación mostrarás un resumen de la conversacion mediante el siguiente contenido descrito entre comillas triples \
            \"\"\" 
            <DETALLE DE LA DEUDA>
            <FORMAS Y LUGARES DE PAGO>
            <SOLICITUD DE RECIBO>
            \"\"\" \
            el campo <DETALLE DE LA DEUDA> <FORMAS Y LUGARES DE PAGO> y <SOLICITUD DE RECIBO> serán proporcionado por la asistentesiempre y cuando hayan sido solicitados previamente\
            de lo contrario el campo quedará vacio \
            la informacion obtenida será delimitada por triples comillas invertidas.\

            mensaje del usuario: ```{message}```
            """
    return prompt