from services.data_service import get_id_from_series_data, create_values_db, give_values_to_serie, create_serie_metadata
def main():
    # Primero se tiene que cargar todo incluido la configuración y las bases de datos
    # Luego se muestran las funciones disponibles y se ejecuta la función seleccionada
    # Las funciones se verán de tal manera que se cree una interfaz de usuario en la terminal para que el usuario pueda interactuar con el programa 
    # La distribución de la interfaz de usuario será la siguiente:
    # Habrá un grupo de botones que representarán las funciones disponibles, y al seleccionar uno de ellos se mostrará un formulario para que el usuario pueda ingresar los datos necesarios para ejecutar la función seleccionada.
    # También se mostrará un botón para volver al menú principal y otro para salir del programa (arriba a la izquierda y arriba a la derecha respectivamente)
    create_values_db()
    create_serie_metadata
    give_values_to_serie
    name = "hola"
    get_id_from_series_data(name)
    
    pass

if __name__ == "__main__":
    main()
