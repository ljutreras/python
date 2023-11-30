""" 
usuario = input("\nIngresa tu nombre: ").lower()

contador = 0
while usuario != "ignacio":
    contador += 1
    if contador > 2:
        print("\nSuperaste el numero de intentos disponibles, lo sentimos\n")
        break
    print("\nNombre incorrecto")
    usuario = input("\nIngresa tu nombre: ").lower()

 """


max_intentos = 3
mensaje =""
breaker = ""
for _ in range(max_intentos):

    if mensaje == "exit":
            break
    usuario = input("\nIngresa tu nombre: ").lower()
    
 
    if usuario == "ignacio":

        print("\n¡Nombre correcto!")

        while mensaje != "exit":

            print("\nEl mensaje es distinto de exit")
            mensaje = input("\nEscribe un mensaje: ").lower()

    else:
        print("\nNombre incorrecto")

if usuario != "ignacio":
    print("\nSuperaste el número de intentos disponibles, lo sentimos\n")



