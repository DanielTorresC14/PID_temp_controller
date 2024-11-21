// Inicio
main()


/**
 * Funcion principal.
 */
function main () {
    document.getElementById("plot").src = `/plot?timestamp= ${new Date().getTime()}`
    setTimeout(main, 300)
}


/**
 * 
 */
function refresh () {

}