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
    generar_grafica()
    return render_template("index.html")



@app.route("/plot")
def get_plot ():
    return flask.send_file("plot.svg", mimetype="image/svg+xml")



@app.route("/current_values", methods=["GET"])
def current_values():
    with open("json_files/data.json", "r") as file:
        values = json.load(file)
    return flask.make_response(values), 200



@app.route("/new_setpoint", methods=["GET"])
def new_setpoint ():
    global setpoint
    value = flask.request.args.get("setpoint")
    setpoint = value

    with open("json_files/data.json") as file:
        values = json.load(file)
        values["targetTemp"] = int(setpoint)

    with open("json_files/data.json", "w") as file:
        json.dump(values, file, indent=4)

    return flask.make_response({"message": "Success!"}), 200



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
        return jsonify({
            'setpoint': setpoint,
            "response": "Data recived successfully! :D"
            }), 200
    print("No se enviaron datos o el formato no es JSON")
    return jsonify({'error': 'No se enviaron datos'}), 400



# TODO remove this method later.
def generar_grafica():
    try:
        # Leer los datos del archivo JSON.
        with open(filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            temps = np.array([])
            brightness = np.array([])
            for row in reader:
                temps = np.append(temps, float(row[0]))
                brightness = np.append(brightness, float(row[1]))
        times = np.arange(0, len(temps))
        
        # Crear la gráfica.
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(times, temps, lw=0.75, label='Real Data', c='#00ffff')
        ax.set_title("Response", c='white')
        ax.set_xlabel("Time t (seg)", c='white')
        ax.set_ylabel("Temperature T (°C)", c='white')

        ax.grid(True, c='#757575', lw=0.5)
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        plt.legend(loc='lower right')

        # Ajustar márgenes de la gráfica.
        plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.15)
        
        # Guardar la gráfica como un archivo SVG.
        plt.savefig("plot.svg", format="svg", dpi=300, bbox_inches='tight', transparent=True)
        print("Gráfica generada y guardada como 'plot.svg'.")
    
    # Posibles Excepciones.
    except FileNotFoundError:
        print("Error: El archivo 'data/data.json' no se encuentra.")
    except Exception as e:
        print(f"Error inesperado: {e}")



def refresh_values ():
    with open("json_files/data.json") as file:
        values = json.load(file)
        with open("csv_files/csv_data.csv") as file:
            reader = csv.reader(file)
            header = next(reader)
            values["min_temp"] = next(reader)[0]
            values["currentTime"] = len([row for row in reader]) + 1
            
    with open("json_files/data.json", "w") as file:
        json.dump(values, file)



# Iniciar servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)