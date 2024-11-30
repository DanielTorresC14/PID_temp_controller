// Inicio
main()

/**
 * Funcion principal.
 */
function main() {
	// Iniciar actualizaciones de datos.
	start()

	// Abrir la entrada del usuario.
	document.getElementById("range").addEventListener("change", function () {
		let setpoint = document.getElementById("range").value
		fetch(`/new_setpoint?setpoint=${setpoint}`)
	})
}

/**
 * Función para iniciar el bucle de actualización de la imagen.
*/
function start() {
	// Iniciar actualización de la gráfica.
	refreshPlot()
	// Iniciar actualización de valores.
	refreshValues()

	// Función que actualiza los valores en la página.
	function refreshValues() {
		// Hacer una solicitud fetch para obtener los datos en formato JSON.
		fetch('/current_values')
			.then(response => response.json())  // Convierte la respuesta a JSON.
			.then(data => {
				// Actualizar los valores en la página con los datos obtenidos.
				document.querySelector(".temperature-section .current-values span:nth-child(1)").textContent = `${data.intensity} %`
				document.querySelector(".temperature-section .current-values span:nth-child(2)").textContent = `${data.setpoint}°C`
				document.getElementById("min_temp").textContent = `${data.min_temp}°C`
				document.querySelector(".temperature-section .maximum-values span:nth-child(2)").textContent = `${data.max_temp}°C`

				// Recargar los valores cada segundo.
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
		var next_second = 1000 - new Date().getMilliseconds();
		document.getElementById("plot").src = `/plot?timestamp=${new Date().getTime()}`;
		setTimeout(refreshPlot, next_second);
	}
}