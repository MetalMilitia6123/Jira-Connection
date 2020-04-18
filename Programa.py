from jira import JIRA
import os 
import shutil
import urllib3

#desactivar el warning de certificado no confiable en la conexion al server
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#constantes
initial_dir = 'C:\\Users\\'
objetivo = "DatosConexionJira.txt"
adjuntos = "\\Adjuntos\\"
ok = "\\ProcesadoOK\\"
error = "\\ProcesadoError\\"
ticket = "TICKET-"

#funciones

def buscar_archivo_DatosConexionJira(x, y):
    #buscar archivo DatosConexionJira.txt del disco C:\\Users\\ del usuario
    for root, _, files in os.walk(x):
        if y in files:
            path = os.path.join(root, y)
            rutaJira_Autom = root
            break
    
    return path, rutaJira_Autom

def armar_ruta(x, y):
    sep = '\\'
    rutafinal = (x + sep + y)
    return rutafinal

def leer_archivo_DatosConexionJira(path):
    #ejemplo de contenido de DatosConexionJira:
    #https://XX.X.XXX.XX
    #XXXXX01
    #Pass001
    archivo = open(path, "r")
    read_file = archivo.readlines()
    archivo.close()
    servidor = read_file[0].strip()
    usuario = read_file[1].strip()
    password = read_file[2].strip()
    return servidor,usuario,password


path, rutaJira_Autom  = buscar_archivo_DatosConexionJira(initial_dir,objetivo)

#armar las rutas
carpAdj = armar_ruta(rutaJira_Autom, adjuntos)
carpOk = armar_ruta(rutaJira_Autom, ok)
carpError = armar_ruta(rutaJira_Autom, error)

#leer archivo Datos conexion para obtener servidor usuario password
servidor, usuario, password = leer_archivo_DatosConexionJira(path)

#Conexion a Jira pasando el server, usuario y pass obtenida del archivo DatosConexion.txt
jira = JIRA(options = {'server': servidor,'verify': False}, basic_auth=(usuario, password))

ruta = os.listdir(carpAdj)
for i in ruta:
    nombre_archivo = i
    pos = nombre_archivo.find(ticket)
    #pos > - 1 = a archivo con numero de ticket
    if pos > -1:
        #Obtengo el numero de ticket y lo guardo en nticket - el formato de ticket es: TICKET-XXXXXX
        nticket = nombre_archivo[pos:pos+13]
        archmov = armar_ruta(carpAdj, nombre_archivo)
        #se arma ubicacion del archivo
        jira.add_attachment(issue=nticket, attachment=archmov)
        print("Se adjunto el archivo:", nombre_archivo)
        shutil.move(os.path.join(carpAdj, nombre_archivo), os.path.join(carpOk, nombre_archivo))
    else: 
        #trato los adjuntos que no tienen numero de ticket 
        archmov = armar_ruta(carpAdj, nombre_archivo)
        #se envia archivo a carpeta error
        print("No se adjunto el archivo:", nombre_archivo)
        shutil.move(os.path.join(carpAdj, nombre_archivo), os.path.join(carpError, nombre_archivo))









