#!/usr/bin/env python
# -*- coding: utf8 -*-
# Authors: Diego Fonzo - Juan P. Ruffino

import RPi.GPIO as GPIO
import MFRC522
import signal

global exit

# Crear un objeto de la clase MFRC522
MIFAREReader = MFRC522.MFRC522()

# Captura SIGINT y limpia GPIO al abortar
def end_read(signal,frame):
    global continue_reading
    print "Bye!"
    continue_reading = False
    GPIO.cleanup()

# Hook de SIGINT para limpiar GPIO al interrumpir el script
signal.signal(signal.SIGINT, end_read)

def read_tag_rfid_specific_block():

	continue_reading = True

	# Ingreso de bloque que se desee leer
	input_block = int(raw_input("Ingrese el Bloque que desea leer: "))
	print("Bloque ingresado: " + str(input_block))

	# Clave de autenticacion por defecto
	key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
	print("Key utilizada: " + ",".join(map(lambda x:str(x),key)))

	# Ciclo que se mantiene leyendo constantemente por tags
	while continue_reading:

    		# Escanea si exista una tag cerca    
    		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    		# Si encuentra una tag...
    		if status == MIFAREReader.MI_OK:
        		print "Tarjeta detectada"

    		# Obtiene el UID de la tag
    		(status,uid) = MIFAREReader.MFRC522_Anticoll()

    		# Si se logro obtener el UID...
    		if status == MIFAREReader.MI_OK:

        		print "UID de tarjeta: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        		# Seleccionar la tag que se va a utilizar
        		MIFAREReader.MFRC522_SelectTag(uid)

        		# Autenticar la operacion en el bloque de la tag
        		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, int(input_block), key, uid)

			# Si la autenticacion es correcta...
        		if status == MIFAREReader.MI_OK:

            			print("Dump ASCII del Bloque " + str(input_block))
           			MIFAREReader.MFRC522_Read(input_block)

            			print("Dump Chars del Bloque " + str(input_block))
            			MIFAREReader.MFRC522_ReadChars(input_block)

            			MIFAREReader.MFRC522_StopCrypto1()
				continue_reading = False
        		else:
            			print("Error de autenticacion")
            			pass

def read_tag_rfid_all_blocks_ascii():
	
	continue_reading = True

	# Ciclo que se mantiene leyendo constantemente por tags
	while continue_reading:

    		# Escanea por tags RFID    
    		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    		# Si se detecta una tag en el lector
    		if status == MIFAREReader.MI_OK:
        		print "Tarjeta detectada"

    		# Obtiene el UID de la tarjeta en el lector
    		(status,uid) = MIFAREReader.MFRC522_Anticoll()

    		# Si se obtuvo el UID continuar
    		if status == MIFAREReader.MI_OK:

        		# UID
        		print "UID de Tarjeta: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        		# Clave para autenticacion por defecto
        		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		
			# Selecciona el tag RFID a leer
        		MIFAREReader.MFRC522_SelectTag(uid)

        		# Dump de datos en ascii
        		MIFAREReader.MFRC522_DumpClassic1K(key, uid)

        		# Fin
        		MIFAREReader.MFRC522_StopCrypto1()

        		continue_reading = False

def read_tag_rfid_all_blocks_chars():

	continue_reading = True

	# Ciclo que se mantiene leyendo constantemente por tags
	while continue_reading:

    		# Escanea por tags RFID    
    		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    		# Si se detecta una tag en el lector
    		if status == MIFAREReader.MI_OK:
        		print "Tarjeta detectada"

    		# Obtiene el UID de la tarjeta en el lector
    		(status,uid) = MIFAREReader.MFRC522_Anticoll()

    		# Si se obtuvo el UID continuar
    		if status == MIFAREReader.MI_OK:

        		# UID
        		print "UID de Tarjeta: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        		# Clave para autenticacion por defecto
        		key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
		
			# Selecciona el tag RFID a leer
        		MIFAREReader.MFRC522_SelectTag(uid)

        		# Dump de datos en chars
        		MIFAREReader.MFRC522_DumpCharsClassic1K(key, uid)

        		# Fin
        		MIFAREReader.MFRC522_StopCrypto1()

        		continue_reading = False

def read_tag_rfid():
	actions = {"1": read_tag_rfid_specific_block, "2": read_tag_rfid_all_blocks_ascii, "3": read_tag_rfid_all_blocks_chars}
	while True:
		print("""
	1) Leer un bloque particular del Tag RFID
	2) Leer el Tag RFID completo (ASCII)
	3) Leer el Tag RFID completo (Chars)
	4) Volver
			""")
		selection = raw_input("Su eleccion: ")
		if selection == "4":
			break
		toDo = actions.get(selection, no_such_action)
		toDo()

def write_tag_rfid_specific_block():

	# Ingreso de los datos que se desean escribir (16 bytes)
	print("Ingrese en ASCII los 16 bytes a escribir: ")
	i = 0
	data = []
	while i < 16:
    		input_data = raw_input("Byte " + str((i+1)) + " :")
    		hexa_data = int(input_data)
    		data.append(hexa_data)
    		i = i+1

	print("Datos ingresados: " + ",".join(map(lambda x:str(x),data)))

	# Ingreso de bloque que se desee escribir
	input_block = int(raw_input("Ingrese el Bloque que desee escribir: "))
	print("Bloque ingresado: " + str(input_block))

	# Clave de autenticacion por defecto
	key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
	print("Key utilizada: " + ",".join(map(lambda x:str(x),key)))

	continue_reading = True

	# Ciclo que se mantiene leyendo constantemente por tags
	while continue_reading:

    		# Escanea si existe una tag cerca
    		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    		# Si se encunetra una tag...
    		if status == MIFAREReader.MI_OK:
        		print "Tarjeta detectada"

    		# Obtiene el UID de la tag
    		(status,uid) = MIFAREReader.MFRC522_Anticoll()

    		# Si se logro obtener el UID...
    		if status == MIFAREReader.MI_OK:

        		print "UID de tarjeta: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        		# Seleccionar la tag que se va a utilizar
        		MIFAREReader.MFRC522_SelectTag(uid)

			# Autenticar la operacion en el bloque de la tag
        		status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, int(input_block), key, uid)

        		# Si la autenticacion es correcta...
        		if status == MIFAREReader.MI_OK:

           			# Mostrar valor anterior y escribir
            			print("Valor ASCII actual del Bloque " + str(input_block))
            			MIFAREReader.MFRC522_Read(input_block)
            			print("Valor Chars actual del Bloque " + str(input_block))
            			MIFAREReader.MFRC522_ReadChars(int(input_block))
				print("Escribiendo...")
            			MIFAREReader.MFRC522_Write(int(input_block), data)
            			
                        	# Verificar los datos escritos
            			print("Ahora el Bloque " + str(input_block) + " posee el siguiente valor:")
            			print("Valor ASCII: ")
            			MIFAREReader.MFRC522_Read(int(input_block))
            			print("Valor Chars: ")
            			MIFAREReader.MFRC522_ReadChars(int(input_block))

            			# Terminar la comunicacion
            			MIFAREReader.MFRC522_StopCrypto1()

            			# Finalizar la lectura de tags
            			continue_reading = False
        		else:
            			print("Error de autenticacion")

def write_tag_rfid():
	actions = {"1": write_tag_rfid_specific_block}
	while True:
		print("""
	1) Escribir un sector particular del Tag RFID
	2) Volver
			""")
		selection = raw_input("Su eleccion: ")
		if selection == "2":
			break
        	toDo = actions.get(selection, no_such_action)
        	toDo()

def no_such_action():
	print("Opcion invalida")
	pass

def main():
    actions = {"1": read_tag_rfid, "2": write_tag_rfid}
    while True:
        print("""
  ___ ___                __     ____ ___________          _____________________
 /   |   \_____    ____ |  | __/  _ \\\_   _____/_ __  ____\______   \_   _____/
/    ~    \__  \ _/ ___\|  |/ />  _ </\    __)|  |  \/    \|       _/|    __)  
\    Y    // __ \\\  \___|    </  <_\ \/     \ |  |  /   |  \    |   \|     \   
 \___|_  /(____  /\___  >__|_ \_____\ \___  / |____/|___|  /____|_  /\___  /   
       \/      \/     \/     \/      \/   \/             \/       \/     \/    

       Seleccione la opcion que desee:

       1) Leer Tag RFID
       2) Escribir Tag RFID
       3) Salir
			""")
        selection = raw_input("Su eleccion: ")
        if selection == "3":
		GPIO.cleanup()
        	return
        toDo = actions.get(selection, no_such_action)
        toDo()

if __name__ == "__main__":
    main()
