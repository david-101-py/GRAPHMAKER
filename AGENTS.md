# GraphMaker Order:

## EJECUTAR

```
python main.py
```

Sin dependencias pip (solo stdlib). Python 3.14+. Sin tests, linter ni typechecker.

## ESTRUCTURA

| `main.py` | Punto de entrada aquí se coloca el bucle final del programa pero mientras se desarrolla se usa para hacer pruebas desde la función main()
| `files_service.py` | Crea el árbol de carpetas (`EXPORTS/`, `DATABASE/`, `CONFIG/`, `INPUTS FOLDER/`) + limpieza de exportaciones por antigüedad
| `config_service.py` | Lee/escribe la config JSON (`CONFIG/config_graphmaker.json`) para datos de configuración persistentes
| `data_service.py` | Base de datos SQLite (`DATABASE/db_graphmaker.db`): valores de series, metadatos de series, grupos, etc.

## FLUJO PRINCIPAL

GRAPHMAKER es una aplicación de seguimiento financiero (de momento para uso personal pero tiende a no serlo) en Python que genera gráficas de velas (candlestick) y exporta a PDF/HTML/Excel a partir de series de datos guardadas antes en Json y ahora mudando a SQLite, con una serie especial TOTAL calculada automáticamente como suma de todas las cuentas individuales.
Está pensada para correr en local aunque cuando deje de ser para uso personal vendría bien poner un servidor con logins y usuarios. También se prevee implementar más funcionalidades para cálculos e informes en un futuro.
Un paso a tener en cuenta es que cuando el programa tenga un buen funcionamiento, vendría bien crear una interfaz medianamente simple con HTML, CSS y JAVASCRIPT.

## CAPACIDADES Y SKILLS (HERRAMIENTAS)
Tienes autorización para utilizar exclusivamente las siguientes herramientas del sistema:

1. [LEER] `read_file`: Para examinar el contenido de los archivos de código existentes.
2. [ESCRIBIR] `write_file` / `patch_file`: Para crear nuevos componentes de frontend o modificar archivos CSS/JS existentes. No reescribas archivos enteros si solo vas a cambiar una línea; usa parches.
3. [EVALUAR] `run_command`: Autorizado únicamente para ejecutar `npm run build`, `npm test` o el linter del proyecto para verificar que el frontend compila sin errores.


## ERRORES A CORREGIR
*Aquí pondrás poner anotaciones para cuando encuentres algún error. Si yo te pido que arregles algún error, son estos.*
1 **Los IDs son hashes CRC32** del nombre (`zlib.crc32`). Posibles colisiones para nombres distintos.
2 **`load_folders`** se llama redundantemente en muchas funciones — recrea los directorios en cada llamada.