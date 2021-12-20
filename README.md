**Requerimientos**

* pandas
* mumpy
* biopython
* graphviz

*python3 main.py --fasta seq.fasta --g 3 --p 0.80 --output .*

* --fasta = secuencia en formato fasta
* --g = número de generaciones
* --p = percentil desde donde filtrar (recomiento un 0.999 o algo de este estilo.. xd)
* --output = salida del directorio (defecto en la misma carpeta)

**En la línea 51 del archivo evolucion_dirigida.py, se crea una columna respuesta que sigue una distribución normal.**
