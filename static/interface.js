// Esperar a que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener('DOMContentLoaded', function () {
    main();
});

/**
 * Función principal.
 */
function main() {
    
}

/**
 * Función para iniciar el bucle de actualización de la imagen y los valores.
 */
function main() {
    // Iniciar actualización de la gráfica.
    refreshPlot()
    // Iniciar actualización de valores.
    refreshValues()

    // Abrir la entrada del usuario.
    document.getElementById("range").addEventListener("change", function () {
        let setpoint = document.getElementById("range").value
        fetch(`/new_setpoint?setpoint=${setpoint}`)
		refreshValues()
    })

    // Función que actualiza los valores en la página.
    function refreshValues() {
        // Hacer una solicitud fetch para obtener los datos en formato JSON desde el servidor Flask
        fetch('/current_values')  // Asegúrate de que el puerto y la URL sean correctos
            .then(response => response.json())  // Convierte la respuesta a JSON
            .then(data => {
                // Actualizar los valores en la página con los datos obtenidos
                document.getElementById("current_temp").textContent = `${data.intensity} %`
                document.getElementById("target_temp").textContent = `${data.setpoint}°C`
                document.getElementById("min_temp").textContent = `${data.min_temp}°C`
                document.getElementById("max_temp").textContent = `${data.max_temp}°C`
                document.getElementById("current_time").textContent = `${data.currentTime} s`
				document.getElementById("target_temp").textContent = `${data.targetTemp}°C`

                // Recargar los valores cada segundo
                setTimeout(refreshValues, 1000)
            })
            .catch(error => {
                console.error('Error al actualizar los valores:', error)
            })
    }

    /**
     * Actualiza la imagen.
     */
    function refreshPlot() {
        var next_second = 1000 - new Date().getMilliseconds()
        document.getElementById("plot").src = `/plot?timestamp=${new Date().getTime()}`
        setTimeout(refreshPlot, next_second)
    }
}