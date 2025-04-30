import xml.sax  # Para procesar archivos XML usando el modelo SAX.
import pandas as pd  # Para manipulación y análisis de datos.
import argparse  # Para manejar argumentos de línea de comandos.
import os  # Para interactuar con el sistema de archivos.

# Clase que hereda de xml.sax.ContentHandler para manejar eventos SAX.
class CustomizationHandler(xml.sax.ContentHandler):
    def __init__(self):
        # Inicializa variables para almacenar datos y controlar el flujo.
        self.data = []  # Lista para almacenar datos extraídos del XML.
        self.current_element = ""  # Almacena la etiqueta actual que se está procesando.
        self.owner_path = None  # Para almacenar el valor de <xt:path>.
        self.env_value_type = None  # Para almacenar el valor de <xt:envValueType>.
        self.value = None  # Para almacenar el valor de <xt:value>.
        self.to_column = None  # Para almacenar el valor de la columna TO.
        self.relevant_types = {  # Conjunto de tipos relevantes que se moverán a TO.
            "Read Timeout for HTTP Outbound Transport Provider",
            "Connection Timeout for HTTP Outbound Transport Provider",
            "SB_ENV_OUTBOUND_TIMEOUT",
            "Service Retry Iteration Interval",
        }

    # Método llamado al encontrar una etiqueta de apertura en el XML.
    def startElement(self, name, attrs):
        self.current_element = name  # Actualiza la etiqueta actual.
        if name == "xt:owner":
            # Reinicia owner_path al entrar a una nueva sección de <xt:owner>.
            self.owner_path = None
        elif name == "xt:replace":
            # Reinicia variables específicas del bloque <xt:replace>.
            self.env_value_type = None
            self.value = None
            self.to_column = None

    # Método llamado al encontrar una etiqueta de cierre en el XML.
    def endElement(self, name):
        if name == "xt:replace":
            # Si el tipo es relevante, mover el valor a la columna TO.
            if self.env_value_type in self.relevant_types:
                self.to_column = self.value  # Mover el contenido de <xt:value> a TO.
                self.value = ""  # Dejar vacía la columna value.
            # Agregar los datos procesados a la lista general.
            self.data.append({
                "owner_path": self.owner_path,
                "envValueType": self.env_value_type,
                "value": self.value,
                "TO": self.to_column
            })
        self.current_element = ""  # Reinicia la etiqueta actual.

    # Método llamado para procesar texto entre etiquetas.
    def characters(self, content):
        content = content.strip()  # Elimina espacios innecesarios.
        if not content:
            return  # Ignora contenido vacío.

        # Almacena valores según la etiqueta actual.
        if self.current_element == "xt:path":
            self.owner_path = content  # Almacena el contenido de <xt:path>.
        elif self.current_element == "xt:envValueType":
            self.env_value_type = content  # Almacena el contenido de <xt:envValueType>.
        elif self.current_element == "xt:value":
            self.value = content  # Almacena el contenido de <xt:value>.

# Función para procesar un archivo XML y exportar los resultados a Excel.
def process_large_xml(xml_file_path, excel_output_path=None):
    # Instancia del manejador personalizado.
    handler = CustomizationHandler()
    # Crea un parser XML y asigna el manejador.
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    # Abre y procesa el archivo XML.
    with open(xml_file_path, "r", encoding="utf-8") as file:
        parser.parse(file)

    # Convierte los datos en un DataFrame de pandas.
    df = pd.DataFrame(handler.data)

    # Define la ruta de salida si no se especifica.
    if not excel_output_path:
        excel_output_path = os.path.join(os.getcwd(), "output.xlsx")

    # Exporta el DataFrame a un archivo Excel.
    df.to_excel(excel_output_path, index=False)
    print(f"Archivo procesado y exportado a {excel_output_path}")

# Punto de entrada principal del programa.
if __name__ == "__main__":
    # Configura argumentos de línea de comandos.
    parser = argparse.ArgumentParser(description="Procesar XML grande y exportar a Excel.")
    parser.add_argument("-f", "--file", required=True, help="Ruta del archivo XML de entrada.")
    parser.add_argument("-o", "--output", help="Ruta del archivo Excel de salida (opcional).")

    # Lee los argumentos proporcionados.
    args = parser.parse_args()

    # Procesa el archivo XML con los argumentos proporcionados.
    process_large_xml(args.file, args.output)