import json
from flask import Flask, render_template
import flask
import matplotlib.pyplot as plt
import numpy as np



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



@app.route("/send", methods=["POST"])
def get_data ():
    data = flask.request.json

    with open("data/data.json", "r") as file:
        localdata = json.load(file)

    with open("data/data.json", "w") as file:
        localdata["temp"] = data["temp"] + localdata["temp"]
        localdata["time"] = data["time"] + localdata["time"]
        print(localdata)
        json.dump(localdata, file)

    generar_grafica()

    return flask.make_response(), 200



# TODO remove this method later.
def generar_grafica():
    try:
        # Leer los datos del archivo JSON
        with open("data/data.json", "r") as file:
            datos = json.load(file)
        
        # Extraer los ejes x (time) y y (temp)
        tiempo = np.array(datos["time"])  # Eje x
        temperatura = np.array(datos["temp"])  # Eje y
        
        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(tiempo, temperatura, label="Temperatura (°C)", color='#FF6347')
        
        # Personalización de la gráfica
        ax.set_title("Temperatura en el tiempo", fontsize=10, color='#FFFFFF')
        ax.set_xlabel("Tiempo (segundos)", fontsize=8, color='#FFFFFF')
        ax.set_ylabel("Temperatura (°C)", fontsize=8, color='#FFFFFF')
        ax.legend(fontsize=8, facecolor='white', edgecolor='white')
        
        # Ajustar los colores de los bordes y ticks
        for spine in ax.spines.values():
            spine.set_color('#FFFFFF')
        ax.xaxis.set_tick_params(colors='#FFFFFF')
        ax.yaxis.set_tick_params(colors='#FFFFFF')
        
        # Agregar una cuadrícula
        ax.grid(True, color='#FFFFFF', linestyle='-', linewidth=0.5)
        
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
    app.run(debug=True, host="0.0.0.0", port=8080)