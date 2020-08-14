from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#import tkMessageBox
import serial, time


def scanear_puertosSerie(num_ports = 20, verbose=False):
    
     #-- Lista de los dispositivos serie. Inicialmente vacia
     dispositivos_serie = []
     
     if verbose:
       print (f"Escaneando {num_ports} puertos serie:") 
     
     #-- Escanear num_port posibles puertos serie
     for i in range(num_ports):
     
       if verbose:
         sys.stdout.write(f"puerto {i}: " )
         sys.stdout.flush()
     
       try:
       
        #-- Abrir puerto serie
        s = serial.Serial(f"COM{i}", 9600)
        
        if verbose: print (f"OK --> {s.portstr}")
        
        #-- Si no hay errores, anadir el numero y nombre a la lista
        dispositivos_serie.append( (i, s.portstr))
        
        #-- Cerrar puerto
        s.close()
             
       #-- Si hay un error se ignora      
       except:
         if verbose: print ("NO")
         pass
         
     #-- Devolver la lista de los dispositivos serie encontrados    
     return dispositivos_serie
 
###########################

puertos_disponibles=scanear_puertosSerie(num_ports=20,verbose=False)

detectados = []
if len(puertos_disponibles)!=0:
    for n,nombre in puertos_disponibles:
        detectados = detectados + [nombre]

###########################

root = Tk()
root.title("Bombillo Arduino")

inicialframe = ttk.Frame(root, padding="3 3 12 12")
inicialframe.grid(column=0, row=0, sticky=(N, W, E, S))

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

############ SELECCIÓN DE PUERTO SERIE ###############
Label(inicialframe, text = "Programa hecho por: Julián Santiago Garnica Castillo - 1103").grid(column=0, row=0)
Label(inicialframe, text = "La Salle Zipaquirá").grid(column=1, row=0)

Label(inicialframe, text = "Seleccione el puerto donde está conectado el Arduino:").grid(column=0, row=1)
Label(inicialframe, text = "(El programa se puede bloquear si el puerto no es \n válido)").grid(column=0, row=2)


try:
  comboCOM = ttk.Combobox(inicialframe, 
                              values=detectados)
  comboCOM.grid(column=1, row=1)
  comboCOM.current(0)

  arduino = serial.Serial()
except TclError:
    messagebox.showerror("Error!", "Ningún puerto COM detectado, vuelva a abrir el programa")
    exit()

validante = 0

def validar_puerto(numero):
  try:
    puerto = comboCOM.get()
    ###Abrir conexión con ARDUINO
    global arduino, validante
    arduino = serial.Serial(puerto, 9600, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False)
    time.sleep(2)

    accion_bytes = bytes(str(numero), encoding= 'utf-8')
    arduino.write(accion_bytes)

    """
    while True:
      data_raw = arduino.readline()
      print(data_raw)
    """
    if(arduino.readline() == b'Confirmado\r\n'):
      messagebox.showinfo("Conexión exitosa","Conectado correctamente con el Arduino!")
      validante = 1
    else:
      messagebox.showerror("Error!", "Error al comprobar conexión con Arduino, asegúrese que el Arduino está bien configurado y verifique el puerto.")
      validante = 0

  except serial.serialutil.SerialException:
    messagebox.showerror("Error!", "Error al comprobar conexión con Arduino, asegúrese que el Arduino está bien configurado y verifique el puerto.")

ttk.Button(inicialframe, text="Validar puerto", command=lambda: validar_puerto(99)).grid(column=1, row=2, sticky=W)

############Funciones de visualización###############

def bombillo(numero):
  try:
    if(validante == 1):
      accion_bytes = bytes(str(numero), encoding= 'utf-8')
      arduino.write(accion_bytes)
      if(numero == 12):
        messagebox.showinfo("Info. Bombillo","Bombillo prendido")
      elif(numero == 13):
        messagebox.showinfo("Info. Bombillo","Bombillo apagado")
    else: messagebox.showerror("Error!", "Error al comprobar conexión con Arduino, asegúrese que el Arduino está bien configurado y valide el puerto.")
  except:
    messagebox.showerror("Error!", "Error al comprobar conexión con Arduino, asegúrese que el Arduino está bien configurado y valide el puerto.")

def display_7_segmentos(numero):
  try:
    if(validante == 1):
      accion_bytes = bytes(str(numero), encoding= 'utf-8')
      arduino.write(accion_bytes)
      aviso = numero-1
      messagebox.showinfo("Oprimió un número!",f"Mostrando el número {aviso} en display")
    else: messagebox.showerror("Error!", "Error al comprobar conexión con Arduino, asegúrese que el Arduino está bien configurado y valide el puerto.")
  except:
    messagebox.showerror("Error!", "Error al comprobar conexión con Arduino, asegúrese que el Arduino está bien configurado y valide el puerto.")


###########################

ttk.Button(mainframe, text="Prender", command=lambda: bombillo(12)).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Apagar", command=lambda: bombillo(13)).grid(column=3, row=1, sticky=W) 

ttk.Button(mainframe, text="1", command= lambda: display_7_segmentos(2)).grid(column=0, row=2, sticky=W)
ttk.Button(mainframe, text="2", command= lambda: display_7_segmentos(3)).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="3", command= lambda: display_7_segmentos(4)).grid(column=2, row=2, sticky=W)
ttk.Button(mainframe, text="4", command= lambda: display_7_segmentos(5)).grid(column=3, row=2, sticky=W)
ttk.Button(mainframe, text="5", command= lambda: display_7_segmentos(6)).grid(column=4, row=2, sticky=W)

ttk.Button(mainframe, text="6", command= lambda: display_7_segmentos(7)).grid(column=0, row=3, sticky=W)
ttk.Button(mainframe, text="7", command= lambda: display_7_segmentos(8)).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="8", command= lambda: display_7_segmentos(9)).grid(column=2, row=3, sticky=W)
ttk.Button(mainframe, text="9", command= lambda: display_7_segmentos(10)).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="0", command= lambda: display_7_segmentos(1)).grid(column=4, row=3, sticky=W)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)



root.mainloop()