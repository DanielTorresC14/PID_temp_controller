from flask import Flask, render_template
import flask
import matplotlib.pyplot as plt
import numpy as np



app = Flask(__name__)



# MAIN ROUTE
@app.route("/")
def home():
    crear_grafica_temperatura() # TODO remove later.
    return render_template("index.html")



# TODO remove this route later.
@app.route("/plot")
def get_plot ():
    return flask.send_file("plot.svg", mimetype='image/svg+xml')



# TODO remove this method later.
def crear_grafica_temperatura():
    """Esta funcion crea la gráfica, pero se espera recibir de otro módulo.
    Además, idealmente debería estar optimizada para mostrarse en espacios
    pequños poruqe las gráficas por defecto desperdician mucho espacio para los
    bordes y cosas así.
    Este código que creó Chatgpt cumple con esta caraterística.
    """

    t = np.linspace(0, 20, 200)
    temperatura = np.exp(0.1 * t) * np.sin(0.5 * t)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(t, temperatura, label="Temperatura (°C)", color='#FF6347')
    ax.set_title("Temperatura", fontsize=10, color='#FFFFFF')
    ax.set_xlabel("Tiempo (segundos)", fontsize=8, color='#FFFFFF')
    ax.set_ylabel("Temperatura (°C)", fontsize=8, color='#FFFFFF')
    ax.legend(fontsize=8, facecolor='white', edgecolor='white')
    ax.spines['top'].set_color('#FFFFFF')
    ax.spines['right'].set_color('#FFFFFF')
    ax.spines['left'].set_color('#FFFFFF')
    ax.spines['bottom'].set_color('#FFFFFF')
    ax.xaxis.set_tick_params(colors='#FFFFFF')
    ax.yaxis.set_tick_params(colors='#FFFFFF')
    ax.grid(True, color='#FFFFFF', linestyle='-', linewidth=0.5)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.15)
    plt.savefig("plot.svg", format="svg", dpi=300, bbox_inches='tight', transparent=True)



# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)