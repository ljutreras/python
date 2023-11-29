def detalle_de_la_deuda(message):
    prompt = f"""Tu tarea es dar el detalle de la deuda de un usuario
            creando una descripcion que contenga
            DETALLE DE LA DEUDA
            <NOMBRE> Tienes un recibo pendiente de tu servicio
            <MOVIL/HOGAR>
            <NRO_SERVICIO> que venció el
            <DD/MM> por CLP <MONTO_DEUDA>

            los datos dentro de las <> para los campos
            NOMBRE
            NRO_SERVICIO
            DD/MM
            MONTO DEUDA
            deben ser aleatorios
            la informacion obtenida será delimitada por
            triples comillas invertidas.

            datos del usuario: ```{message}```
            """
    return prompt

# OK