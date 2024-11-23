// Inicio
main()


/**
 * Funcion principal.
 */
function main() {
	start()
}


/**
 * Función para iniciar el bucle de actualización de la imagen.
*/
function start() {
	// Obtener elementos.
	// Iniciar recursividad.
	refreshPlot()

	/**
	 * Actualiza la imagen.
	*/
	function refreshPlot() {
		var next_second = 1000 - new Date().getMilliseconds()
		document.getElementById("plot").src = `/plot?timestamp= ${new Date().getTime()}`
		setTimeout(refreshPlot, next_second)
	}
}