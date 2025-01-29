#Este script es utilizado para verificar que librerías tenemos instaladas de manera rápida y sencilla.
#Solo modificando el nombre de la librería a consultar obtenemos la respuesta.

libreria = "openpyxl" #Modificar el String por el nombre de la librería a revisar y ejecutar
try:
    import importlib
    importlib.import_module(libreria) #permite importar una librería usando un string
    print(f"La librería '{libreria}' está instalada.")
except ImportError:
    print(f"La librería '{libreria}' no está instalada.")
