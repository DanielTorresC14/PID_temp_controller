import json
import csv
import flask
import matplotlib.pyplot as plt
import numpy as np

from flask import Flask, request, render_template, jsonify

# Contiene los datos para graficar
filename = "csv_files/csv_data.csv"

# Crea el archivo csv si no existe.
try:
    with open(filename, 'x', newline='') as f:
        write = csv.writer(f)
        write.writerow(['Temperature', 'Brightness'])
except FileExistsError:
    pass

current_temp = 0
setpoint = 0
app = Flask(__name__)

# MAIN ROUTE
@app.route("/")
def home():
    generar_grafica() # TODO remove later.
    return render_template("index.html")



# TODO remove this route later.
@app.route("/plot")
def get_plot ():
    return flask.send_file("plot.svg", mimetype='image/svg+xml')



@app.route("/data", methods=["POST"])
def get_data ():
    global setpoint
    data = request.get_json()
    if data:
        print("Datos recibidos:", data)
        with open(filename, 'a', newline='') as f:
            write = csv.writer(f)
            write.writerow([data['temp'], data['brightness']])
        generar_grafica()
        return jsonify({'setpoint': setpoint}), 200
    print("No se enviaron datos o el formato no es JSON")
    return jsonify({'error': 'No se enviaron datos'}), 400

# TODO remove this method later.
def generar_grafica():
    try:
        # Leer los datos del archivo JSON
        with open("data/data.json", "r") as file:
            datos = json.load(file)
        
        # Extraer los ejes x (time) y y (temp)
        tiempo = np.arange(0, len(datos["temp"]))  # Eje x
        temperatura = np.array(datos["temp"])  # Eje y
        
        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(tiempo, temperatura, label="Temperatura (°C)", color='#FF6347')
        
        # Ajustar márgenes de la gráfica
        plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.15)
        
        # Guardar la gráfica como un archivo SVG
        plt.savefig("plot.svg", format="svg", dpi=300, bbox_inches='tight', transparent=True)
        print("Gráfica generada y guardada como 'plot.svg'.")
    except FileNotFoundError:
        print("Error: El archivo 'data/data.json' no se encuentra.")
    except KeyError as e:
        print(f"Error: La clave '{e.args[0]}' no existe en el archivo JSON.")
    except json.JSONDecodeError:
        print("Error: El archivo JSON tiene un formato inválido.")
    except Exception as e:
        print(f"Error inesperado: {e}")


# Iniciar servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)